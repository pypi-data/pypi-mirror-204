'''
Quarch Power Module Calibration Functions
Written for Python 3.6 64 bit

M Dearman April 2019
Edited k McRobert September 2021
'''
import quarchpy.user_interface

'''
Calibration Flow
    Connect to AC PAM Fixture 
    Connect to ELPA-SINE
    step through each AC phase
      - Read peak voltage value and set voltage multiplier
      - Step through current values and set current multiplier
      - Save neutral current readings
    Calibrate/verify neutral

'''

#Imports QuarchPy library, providing the functions needed to use Quarch modules
#from quarchpy import quarchDevice #, scanDevices

# Import other libraries used in the examples

from .PowerModuleCalibration import *
from .calibrationConfig import *
from .elpaSine import *
from quarchpy.device.device import *
from quarchpy.user_interface import *
from quarchpy.utilities.BitManipulation import *
from quarchpy.device import quarchPPM, quarchDevice
import csv
import numpy as np
from collections import OrderedDict
from .ET2260 import SwitchBoxControl

def parseFixtureData(response,start,length):

    # split the multiline response into a list
    response = response.splitlines()
    result = ""
    # for each line
    for line in response:
        # remove 0x, swap bytes
        line = line[4:6] + line[2:4]
        # convert 4 char Hex to 16 bit binary string
        line = "{0:016b}".format(int(line,16))
        # concatenate all the strings
        result += line
    # pick out the section we want
    result = int(result[start:(start+length)],2)
    # convert two's compliment
    if (result >= 2**(length-1)):
        result -= 2**length
    return result


def bcdString(bcd,padding):
    # strip off "0x" if present
    if bcd[:2] == "0x":
        bcd = bcd [2:]
    # strip off leading 0's
    # loop while we have more the required minimum number of characters left
    while(len(bcd)>padding):
        # if the leading character is 0, remove it
        if bcd[0] == '0':
            bcd = bcd[1:]
        # else exit loop
        else:
            break
    return bcd

currentPhase = None



class QTL2582_Calibration:
    phaseList = ['L1', 'L2', 'L3', 'Neutral']
    calTypeList = ['I', 'V', 'V2']
    CALIBRATION_MODE_ADDR = '0xA100'
    CALIBRATION_CONTROL_ADDR = '0xA101'
    CALIBRATION_COMPLETE_ADDR = '0xA11C'
    voltScalingConstant = 1.0
    currentScalingConstant = 1.0
    test_steps = None
    test_min = None
    test_max = None
    maxElpaCurrent = 5000.0
    calMultiplier = 1.0
    streamMeasureTime = 2.0
    coeffValid = False
    worstCase = 0.0
    relErrorLimit = 1.5
    phase = None
    verification = False
    units = None
    fullName = None
    lastMeasurement = None
    useNumpy = False

    def __init__(self, moduleConnection, calType='I', calPhase='L1', verify=False, neutral=None):
        self.conn = moduleConnection
        self.neutral = neutral
        if moduleConnection is not None:
            self.powerdev = quarchPPM(moduleConnection)
            # Don't need to manually create RMS channels any more
            if not self.useNumpy:
                for phase in self.phaseList:
                    self.powerdev.sendCommand("stream create channel chan({0}vRMS, V) rms(40mS, chan({0}, V) ) mV 1.0".format(phase))
                    self.powerdev.sendCommand("stream create channel chan({0}aRMS, A) rms(40mS, chan({0}, A) ) mA 1.0".format(phase))

        self.streamFilename = None
        self.elpa = None
        self.elpaConnected = False

        self.calType = calType
        self.phase = calPhase

        self.SwitchMux = SwitchBoxControl("AC PAM Mux")
        self.SwitchMux.discover()
        self.SwitchMux.connect()

        if calType == 'I':
            self.absoluteErrorLimit = 0.0
            self.units = "mA"
            self.fullName = "Current"

            if self.verification:
                self.test_steps = 8
                self.test_min = 200.0
                self.test_max = 5000.0
            else:
                self.test_steps = 5
                self.test_min = 1000.0
                self.test_max = 5000.0
        else:
            self.absoluteErrorLimit = 0.0
            self.units = "mV"
            self.fullName = "Voltage"

            self.test_steps = 1
            self.test_min = 340000.0
            self.test_max = 340000.0
        self.verification = verify

    def init(self):
        self.SwitchMux.select_phase(self.phase)
        #global currentPhase
        #if currentPhase != self.phase:
        #    quarchpy.user_interface.showDialog(
        #        "Set power connections to phase " + self.phase + ", verify 240V on ELPA-SINE")
        #    currentPhase = self.phase

    # This call has no meaning for AC PAM voltage calibration, as reference voltages cannot be set
    def setRef(self, x):
        if self.calType == 'I':
            if x < 0 or x > self.maxElpaCurrent:
                raise ValueError("ERROR - ELPA max RMS current must be less than " + self.maxElpaCurrent + " mA")
            self.elpa.setLoadCurrent(x / 1000.0)
            self.elpa.enable()
            time.sleep(0.5)

    def readRef(self):
        if self.calType == 'I':
            self.lastCurrentReading = self.elpa.getCurrentMeasurement('RMS') * 1000.0
            return self.lastCurrentReading
        else:
            return self.elpa.getVoltageMeasurement('RMS') * 1000.0

    def readVal(self):
        # Return measurement, normalize all values to Volts and Amps
        return self.getMeasurement(self.phase, self.calType, typ='RMS', streamTime=self.streamMeasureTime)

    def finish(self):
        self.elpa.disable()

    # Calculate the correct multiplier coefficients
    # Since the AC PAM does not have an offset, use a weighted average of the multiplier values rather than
    # attempting a linear fit
    def generate(self, points):
        multiplierList = []
        multSum = 0.0
        for p in points:
            multiplierList.append(p[1] / p[0])
            multSum += multiplierList[-1]

        mult = multSum / len(points)
        if mult >= 1.0 and mult <= 2.0:
            self.calMultiplier = mult
            self.coeffValid = True
        else:
            self.coeffValid = False
        return self.coeffValid

    def setCoefficients(self):
        self.setMultiplier(self.phase, self.calType, self.calMultiplier)

    def streamData(self, streamTime=1.0):
        # Sets for a manual record trigger, so we can start the stream from the script
        self.powerdev.sendCommand("record:trigger:mode manual")
        self.powerdev.sendCommand("record:averaging 0")

        # In this example we write to a fixed path
        self.streamFilename = 'Stream1.csv'
        self.powerdev.startStream(self.streamFilename, 2000, 'Example stream to file')

        # Delay for a x seconds while the stream is running.  You can also continue
        # to run your own commands/scripts here while the stream is recording in the background
        time.sleep(streamTime)

        # Check the stream status, so we know if anything went wrong during the stream
        streamStatus = self.powerdev.streamRunningStatus()
        if ("Stopped" in streamStatus):
            if ("Overrun" in streamStatus):
                print('Stream interrupted due to internal device buffer has filled up')
            elif ("User" in streamStatus):
                print('Stream interrupted due to max file size has being exceeded')
            else:
                print("Stopped for unknown reason")

        # Stop the stream.  This function is blocking and will wait until all remaining data has
        # been downloaded from the module
        self.powerdev.stopStream()

        # check to ensure stream is fully stopped before continuing script
        stopStreamCount = 0
        while not "stopped" in str(self.powerdev.streamRunningStatus()).lower():
            stopStreamCount += 1
            if stopStreamCount > 20:
                raise TimeoutError("Failed to stop stream after {} seconds".format(stopStreamCount))
            time.sleep(1)

    def getCoeffAddr(self, phase, calType):
        if phase not in self.phaseList:
            raise ValueError("Unknown phase " + phase)
        elif calType not in self.calTypeList:
            raise ValueError("Unknown calibration type " + calType)
        else:
            pnumber = self.phaseList.index(phase) * 3 + self.calTypeList.index(calType)
            addrLow = 0xA105 + pnumber * 2
            addrHigh = addrLow + 1
        return (addrLow, addrHigh)

    def readRawValues(self):
        rawValues = {}
        with open(self.streamFilename, 'r') as fh:
            csvfile = csv.reader(fh)
            titles = None
            for row in csvfile:
                if not titles:
                    titles = row
                    for i in range(len(row)):
                        rawValues[titles[i]] = []
                else:
                    for i in range(len(row)):
                        try:
                            rawValues[titles[i]].append(int(row[i]))
                        except ValueError:
                            rawValues[titles[i]].append(0)
        return rawValues

    def calcRmsValues(self):
        rawValues = self.readRawValues()
        rmsValues = {}
        for k in rawValues.keys():
            if self.useNumpy:
                vec = np.array(rawValues[k][1:-1]).astype(float)
                if len(vec) > 100:
                    rmsValues[k] = np.sqrt(vec.dot(vec) / vec.size)
            else:
                items = [float(x) for x in rawValues[k][1:-1] if x > 0]
                if len(items) > 100:
                    average = sum(items) / float(len(items))
                    rmsValues[k] = average

        self.lastMeasurement = rmsValues
        return rmsValues

    def findPeakValues(self):
        maxvalues = []
        prevValues = []
        peakList = []
        rising = []
        with open(self.streamFilename, 'r') as fh:
            csvfile = csv.reader(fh)
            titles = None
            for row in csvfile:
                if not titles:
                    titles = row
                    for i in range(len(row)):
                        maxvalues.append(0)
                        prevValues.append(0)
                        peakList.append([])
                        rising.append(False)
                else:
                    for i in range(len(row)):
                        value = int(row[i])
                        if value >= maxvalues[i]:
                            maxvalues[i] = value

                        # If we are in the positive have of the wave, look for the point just when values begin to fall
                        if value > 0:
                            if value > prevValues[i]:
                                rising[i] = True
                                prevValues[i] = value
                            else:
                                if rising[i]:
                                    peakList[i].append(prevValues[i])
                                    rising[i] = False
                        else:
                            # On the negative half of the wave, reset the values for the next pass
                            rising[i] = False
                            prevValues[i] = 0

        mvdict = {}
        avgPeak = {}
        for i in range(len(titles)):
            mvdict[titles[i]] = maxvalues[i]

            # Throw away first and last samples, as they may have been clipped
            peakVector = np.array(peakList[i][1:-1])
            avgPeak[titles[i]] = peakVector.mean()

        return avgPeak

    def shutdown(self):
        self.powerdev.closeConnection()

    def loadToAde(self):
        self.powerdev.sendCommand("write 0x1000 0x0000")
        self.powerdev.sendCommand("write 0x1000 0x0002")

    def clear_calibration(self):

        # set unit into calibration mode
        self.powerdev.sendCommand("write " + self.CALIBRATION_MODE_ADDR + " 0xaa55")
        self.powerdev.sendCommand("write " + self.CALIBRATION_MODE_ADDR + " 0x55aa")

        # clear all calibration registers
        for phase in self.phaseList:
            for t in ["V", "I", "V2"]:
                caddr = self.getCoeffAddr(phase, t)
                self.powerdev.sendAndVerifyCommand("write 0x{0:04x} 0x0000".format(caddr[0]))
                self.powerdev.sendAndVerifyCommand("write 0x{0:04x} 0x0000".format(caddr[1]))

        self.loadToAde()

        # write 0xaa55 to register to calibration complete register to tell module it is calibrated
        self.powerdev.sendAndVerifyCommand("write " + self.CALIBRATION_COMPLETE_ADDR + " 0xaa55")

    def getStepMultiplier(self):
        if self.test_steps > 1:
            return (self.test_max / self.test_min) ** (1 / self.test_steps)
        else:
            return 2.0

    '''Set the AC PAM multiplier value, which is a 23-bit fixed point number
    '''

    def setMultiplier(self, phase, parm, mult):
        addrLow, addrHigh = self.getCoeffAddr(phase, parm)

        if ((mult < 1.0) or (mult >= 4.0)):
            raise ValueError("Multiplier must be between 1 and 2")
        else:
            mconst = int((mult - 1.0) * (2 ** 23))
            mconst_low = mconst & 0xFFFF
            mconst_high = mconst >> 16
            # print("Setting phase {0} const to {1:06x}".format(phase, mconst))
            self.conn.sendCommand("write 0x{0:04x} 0x{1:04x}".format(addrLow, mconst_low))
            self.conn.sendCommand("write 0x{0:04x} 0x{1:04x}".format(addrHigh, mconst_high))

            # Trigger FPGA to load new values into the ADE7978
            self.loadToAde()

    def getMeasurement(self, phase, parm, typ='PEAK', streamTime=1.0):
        self.streamData(streamTime)
        if typ == 'PEAK':
            vals = self.findPeakValues()
        else:
            vals = self.calcRmsValues()

        if parm == 'V':
            if self.useNumpy:
                key = "{0:s} mV".format(phase)
            else:
                key = "{0:s}vRMS mV".format(phase)
        else:
            if self.useNumpy:
                key = "{0:s} mA".format(phase)
            else:
                key = "{0:s}aRMS mA".format(phase)

        if key in vals:
            if parm == 'I':
                if self.useNumpy:
                    self.neutral.add_measurement(self.lastCurrentReading, vals["N mA"])
                else:
                    self.neutral.add_measurement(self.lastCurrentReading, vals["NeutralaRMS mA"])
            return vals[key]
        else:
            return 0

    def report(self, data):
        report = []

        self.title = "AC PAM Phase {} {} Calibration".format(self.phase, self.fullName)

        report.append("")
        report.append("{0:>20s} {1:>20s} {2:>20s} {3:>20s}".format("DUT Value", "Inst Value", "Abs Error", "Rel Error"))
        worstError = 0.0
        passedVerif = True
        for d in data:
            errorTuple = getError(d[0], d[1], self.absoluteErrorLimit, self.relErrorLimit)
            worstError = max(errorTuple[3], worstError)
            report.append("{0:17.2f} {5:2s} {1:17.2f} {5:2s} {4:>9s}{2:8.2f} {5:2s} {3:20.2f}%".format(d[0], d[1], errorTuple[0], errorTuple[3], errorTuple[1], self.units))
            if errorTuple[4] == False:
                passedVerif = False

        report.append(
            "==================================================================================================")

        if self.verification:
            result = passedVerif
        else:
            result = self.coeffValid
        return {"title": self.title, "result": result, "worst case": "{0:4.2f}%".format(worstError),
                "report": ('\n'.join(report))}

    def write_calibration(self):

        # write the calibration registers
        # erase the tag memory
        printText("Erasing TAG memory..")
        self.powerdev.sendCommand("write 0xa200 0x0020")
        # TODO: should check for completion here...
        # wait for 2 seconds for erase to complete
        # check busy
        while checkBit(self.powerdev.sendCommand("read 0xa200"), 8):
            time.sleep(0.1)
        # write the tag memory
        printText("Programming TAG memory...")
        self.powerdev.sendCommand("write 0xa200 0x0040")
        # check busy
        while checkBit(self.powerdev.sendCommand("read 0xa200"), 8):
            time.sleep(0.1)

class Neutral_Calibration (QTL2582_Calibration):
    def __init__(self, moduleConnection, verify=False):
        super().__init__(moduleConnection=moduleConnection, calType='I', calPhase='Neutral', verify=verify, neutral=None)
        self.verification = verify     # Set to False for calibration, True for verification
        self.measurements = []
        self.absoluteErrorLimit = 0.0
        self.relErrorLimit = 1.5
        self.test_steps = 0
        self.test_min = 100
        self.test_max = 1000
        self.units = "mA"

    def init(self):
        pass

    def setRef(self, x):
        pass

    def readRef(self):
        return self.measurements[0][0]

    def readVal(self):
        val = self.measurements[0][1]
        self.measurements.pop(0)
        return val

    def finish(self):
        pass

    def shutdown(self):
        pass

    def add_measurement(self, ref, val):
        self.measurements.append( (ref, val) )
        self.test_steps = len(self.measurements)
        self.test_max = self.test_min * (2 ** (len(self.measurements)-1))

    def getStepMultiplier(self):
        return 2

    def report(self, data):

        report = []

        self.title = "AC PAM Neutral Calibration"

        report.append("")
        report.append("{0:>20s} {1:>20s} {2:>20s} {3:>20s}".format("DUT Value", "Inst Value", "Abs Error", "Rel Error"))
        worstError = 0.0
        passedVerif = True
        for d in data:
            errorTuple = getError(d[0], d[1], self.absoluteErrorLimit, self.relErrorLimit)
            worstError = max(errorTuple[3], worstError)
            report.append("{0:17.2f} {5:2s} {1:17.2f} {5:2s} {4:>9s}{2:8.2f} {5:2s} {3:20.2f}%".format(d[0], d[1], errorTuple[0], errorTuple[3], errorTuple[1], self.units))
            if errorTuple[4] == False:
                passedVerif = False

        report.append(
            "==================================================================================================")

        if self.verification:
            result = passedVerif
        else:
            result = self.coeffValid
        return {"title": self.title, "result": result, "worst case": "{0:4.2f}%".format(worstError),
                "report": ('\n'.join(report))}

class QTL2582 (PowerModule):
    phaseList = ['L1', 'L2', 'L3', 'Neutral']
    calTypeList = ['I', 'V', 'V2']

    # Fixture Register Addresses
    CALIBRATION_MODE_ADDR               = '0xA100'
    CALIBRATION_CONTROL_ADDR            = '0xA101'

    SAVE_VALUE_START_ADDR               = '0xA102'

    AIGAIN_LOW_ADDR                     = '0xA105'
    AIGAIN_HIGH_ADDR                    = '0xA106'
    AVGAIN_LOW_ADDR                     = '0xA107'
    AVGAIN_HIGH_ADDR                    = '0xA108'
    AV2GAIN_LOW_ADDR                    = '0xA109'
    AV2GAIN_HIGH_ADDR                   = '0xA10A'

    BIGAIN_LOW_ADDR                     = '0xA10B'
    BIGAIN_HIGH_ADDR                    = '0xA10C'
    BVGAIN_LOW_ADDR                     = '0xA10D'
    BVGAIN_HIGH_ADDR                    = '0xA10E'
    BV2GAIN_LOW_ADDR                    = '0xA10F'
    BV2GAIN_HIGH_ADDR                   = '0xA110'

    CIGAIN_LOW_ADDR                     = '0xA111'
    CIGAIN_HIGH_ADDR                    = '0xA112'
    CVGAIN_LOW_ADDR                     = '0xA113'
    CVGAIN_HIGH_ADDR                    = '0xA114'
    CV2GAIN_LOW_ADDR                    = '0xA115'
    CV2GAIN_HIGH_ADDR                   = '0xA116'

    NIGAIN_LOW_ADDR                     = '0xA117'
    NIGAIN_HIGH_ADDR                    = '0xA118'
    NVGAIN_LOW_ADDR                     = '0xA119'
    NVGAIN_HIGH_ADDR                    = '0xA11A'
    NV2GAIN_LOW_ADDR                    = '0xA11B'
    NV2GAIN_HIGH_ADDR                   = '0xA11C'

    CALIBRATION_COMPLETE_ADDR	        = '0xA11D'
    LOAD_VOLTAGE                        = 340000

    # Fixture Information
    PAMSerial = None
    FixtureSerial = None
    calObjectSerial = None     # The serial number of the device that is being calibrated, i.e QTL1944 in HD PPM, Fixture in PAM
    idnStr = None
    Firmware = None
    Fpga = None
    calInstrument = None
    calInstrumentId = None
    switchbox = None

    # Physical Connection Tracking (what is plugged to what)
    loadChannel = None
    hostPowerChannel = None

    # general
    waitComplete = False
    checkedWiring = False
    currentPhase = None

    def specific_requirements(self):

        reportText=""

        if "elpaSine" in calibrationResources.keys():
            elpa = elpaSine(calibrationResources["elpaSine"])
        else:
            # No selection process as of yet, the ELPA-SINE has a static address
            target = quarchpy.user_interface.listSelection(title="Load Selection", message="Select ELPA-SINE unit to connect to",
                                                  selectionList="127.0.0.1=localhost,192.168.1.239=static")
            elpa = elpaSine(target)
        elpa.openConnection()
        self.calInstrument = elpa

        # Check connectivity to the ELPA-SINE
        elpaIdentity = self.calInstrument.sendCommandQuery("*IDN?")
        if elpaIdentity.find("ELPA-SINE") == -1:
            printText("Unable to communicate with ELPA-SINE")
            raise Exception("Unable to communicate with ELPA-SINE")
        self.calInstrumentId = elpaIdentity

        # Connect the individual calibrations to the ELPA
        for calPhase in list(self.calibrations.values()) + list(self.verifications.values()):
            for calItem in calPhase.values():
                calItem.elpa = self.calInstrument

        # Write module specific report header to file
        reportText += "Quarch AC Power Analysis Module: "
        reportText += self.PAMSerial + "\n"
        reportText += "Quarch FW Versions: "
        reportText += "FW:" + self.Firmware + ", FPGA: " + self.Fpga + "\n"
        reportText += "\n"
        reportText += "Calibration Instruments#:\n"
        reportText += self.calInstrumentId + "\n"

        # perform uptime check and write to file
        if self.waitComplete != True:
            reportText += self.wait_for_up_time(desired_up_time=600, command="conf:runtime:fix:sec?")
            self.waitComplete = True

        return reportText

    def setConnections(self,loadConnection,hostPowerConnection,reset=False):
        if hostPowerConnection:
            showDialog("Set source switch to phase {}".format(hostPowerConnection))
        if loadConnection:
            showDialog("Set load switch to phase {}".format(loadConnection))

    def getCoeffAddr(self, phase, calType):
        if phase not in self.phaseList:
            raise ValueError("Unknown phase " + phase)
        elif calType not in self.calTypeList:
            raise ValueError("Unknown calibration type " + calType)
        else:
            pnumber = self.phaseList.index(phase) * 3 + self.calTypeList.index(calType)
            addrLow = 0xA105 + pnumber * 2
            addrHigh = addrLow + 1
            #addrLow = getattr(self, "{0}{1}GAIN_LOW".format(phase, calType))
            #addrHigh = getattr(self, "{0}{1}GAIN_HIGH".format(phase, calType))
        return (addrLow, addrHigh)


    def clear_calibration(self):

        # set unit into calibration mode
        self.dut.sendCommand("write " + QTL2582.CALIBRATION_MODE_ADDR + " 0xaa55")
        self.dut.sendCommand("write " + QTL2582.CALIBRATION_MODE_ADDR + " 0x55aa")

        # clear all calibration registers
        for phase in self.phaseList:
            for t in ["V", "I", "V2"]:
                caddr = self.getCoeffAddr(phase, t)
                self.dut.sendAndVerifyCommand("write 0x{0:04x} 0x0000".format(caddr[0]))
                self.dut.sendAndVerifyCommand("write 0x{0:04x} 0x0000".format(caddr[1]))

        # Load calibration values into the ADE7978
        self.dut.sendCommand("write 0x1000 0x0000")
        self.dut.sendCommand("write 0x1000 0x0002")

        # write 0xaa55 to register to calibration complete register to tell module it is calibrated
        self.dut.sendAndVerifyCommand("write " + QTL2582.CALIBRATION_COMPLETE_ADDR + " 0xaa55")
        
    def write_calibration(self):

        # write the calibration registers
        # erase the tag memory
        printText("Erasing TAG memory..")
        self.dut.sendCommand("write 0xa200 0x0020")
        # TODO: should check for completion here...
        # wait for 2 seconds for erase to complete
        # check busy
        while checkBit(self.dut.sendCommand("read 0xa200"),8):
            sleep(0.1)
        # write the tag memory
        printText("Programming TAG memory...")
        self.dut.sendCommand("write 0xa200 0x0040")        
        # check busy
        while checkBit(self.dut.sendCommand("read 0xa200"),8):
            sleep(0.1)

    def close_module(self):
        #close the connection to the calibration instrument
        self.calInstrument.closeConnection()

    def close_all(self):

        #close all attached devices
        self.calInstrument.setLoadCurrent(0)
        self.calInstrument.closeConnection()
        self.powerModule.setConnections(None,None)


    def __init__(self,dut):

        # set the name of this module
        self.name = "AC PAM"
        self.dut = dut

        # Serial numbers (ensure QTL at start)
        self.enclosureSerial = self.dut.sendCommand("*ENCLOSURE?")
        if (self.enclosureSerial.find ("QTL") == -1):
            self.enclosureSerial = "QTL" + self.enclosureSerial
        # fetch the enclosure position
        self.PAMSerial = self.dut.sendCommand ("*SERIAL?")
        if (self.PAMSerial.find ("QTL") == -1):
            self.PAMSerial = "QTL" + self.PAMSerial
        # Fixture Serial
        # fixture serial is retrieved as BCD, we need to convert and pad it
        self.FixtureSerial = None

        # calObjectSerial Serial
        self.calObjectSerial = self.PAMSerial
        # Filename String
        self.filenameString = self.PAMSerial
        # Code version (FPGA)
        self.idnStr = dut.sendCommand ("*IDN?")
        pos = self.idnStr.upper().find ("FPGA 1:")
        if (pos != -1):
            versionStr = self.idnStr[pos+7:]
            pos = versionStr.find ("\n")
            if (pos != -1):
                versionStr = versionStr[:pos].strip()
            else:
                pass
        else:
            versionStr = "NOT-FOUND"    
        self.Fpga = versionStr.strip()
    
        # Code version (FW)    
        pos = self.idnStr.upper().find ("PROCESSOR:")
        if (pos != -1):
            versionStr = self.idnStr[pos+10:]
            pos = versionStr.find ("\n")
            if (pos != -1):
                versionStr = versionStr[:pos].strip()            
            else:
                pass
        else:
            versionStr = "NOT-FOUND"    
        self.Firmware = versionStr.strip()

        self.calibrations = OrderedDict()
        neutCal = Neutral_Calibration(self.dut, verify=False)
        calPhaseList = ["L1", "L2", "L3"]

        for phase in calPhaseList:
            self.calibrations[phase] = {
                "Voltage" : QTL2582_Calibration(self.dut, calType='V', calPhase=phase, neutral=None),
                "Current" : QTL2582_Calibration(self.dut, calType='I', calPhase=phase, neutral=neutCal)
            }
        self.calibrations["Neutral"] = { "Current" : neutCal }

        self.verifications = OrderedDict()
        neutVerif = Neutral_Calibration(self.dut, verify=True)
        for phase in calPhaseList:
            self.verifications[phase] = {
                "Voltage" : QTL2582_Calibration(self.dut, calType='V', calPhase=phase, verify=True, neutral=None),
                "Current" : QTL2582_Calibration(self.dut, calType='I', calPhase=phase, verify=True, neutral=neutVerif)
            }
        self.verifications["Neutral"] = { "Current" : neutVerif }

