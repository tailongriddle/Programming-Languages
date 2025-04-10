# standard virtual memory page table implementation

# This is a basic implementation of a page table
#   with aging as the replacement policy
# It includes no TLB, multilevel or inverted tables
# It works for multiple processes

# The format of a page table entry is:
#   ---Mbit Rbit Pbit frame#

import math

# This is a helper class that decodes any page table entry given to it
#   so we don't have to have all the bit manipulation in the main code
# This is a helper class that decodes any page table entry given to it
#   so we don't have to have all the bit manipulation in the main code
# Note that since we can't pass integers by reference in Python that
#   we use a modify and return pattern for the functions that modify
class InvertedPageTableDecoder:
    def __init__(self, processBits, pageBits):
        self.processBits = processBits
        self.pageBits = pageBits

    def getModified(self, entry):
        return (entry >> (self.processBits + self.pageBits + 2)) & 1

    def getReferenced(self, entry):
        return (entry >> (self.processBits + self.pageBits + 1)) & 1

    def getPresent(self, entry):
        return (entry >> (self.processBits + self.pageBits)) & 1

    def setModified(self, entry):
        return entry | (1 << (self.processBits + self.pageBits + 2))

    def setReferenced(self, entry):
        return entry | (1 << (self.processBits + self.pageBits + 1))

    def setPresent(self, entry):
        return entry | (1 << (self.processBits + self.pageBits))

    def clearModified(self, entry):
        return entry & ~(1 << (self.processBits + self.pageBits + 2))

    def clearReferenced(self, entry):
        return entry & ~(1 << (self.processBits + self.pageBits + 1))

    def clearPresent(self, entry):
        return entry & ~(1 << (self.processBits + self.pageBits))

    def getProcess(self, entry):
        return (entry >> self.pageBits) & ((1 << self.processBits) - 1)

    def getPage(self, entry):
        return entry & ((1 << self.pageBits) - 1)

    def replaceProcessAndPage(self, entry, process, page):
        # Clear out old process/page bits, then insert the new values
        entry &= ~(((1 << self.processBits) - 1) << self.pageBits | ((1 << self.pageBits) - 1))
        entry |= (process << self.pageBits) | page
        return entry

def displayInvertedPageTable(frames, decoder, agingR):
    print("\nInverted Page Table (with associated aging status):")
    print("frame#\tprocess\tpage#\tmod\tref\tpresent\taging")

    for frameNum, aging in enumerate(agingR):
        found = False

        for entry in frames:
            if decoder.getPresent(entry) and frames.index(entry) == frameNum:
                processNum = decoder.getProcess(entry)
                pageNum = decoder.getPage(entry)
                mod = decoder.getModified(entry)
                ref = decoder.getReferenced(entry)
                present = decoder.getPresent(entry)
                print(f"{frameNum}\t{processNum}\t{pageNum}\t{mod}\t{ref}\t{present}\t{aging}")
                found = True
                break

        if not found:
            print(f"{frameNum}\t-\t-\t-\t-\t-\t-")

def readFile(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    # First line is the number of bits for things
    #  Virtual Address, Physical Address, Page Size
    virBits = int(lines[0].split()[0])
    phyBits = int(lines[0].split()[1])
    pageBits = int(lines[0].split()[2])

    # Second line is the number of processes
    numProcesses = int(lines[1])
    
    # Remove the first two lines
    lines = lines[2:]

    return virBits, phyBits, pageBits, numProcesses, lines

def selectReplacementFrame(agingR):
    frameToReplace = agingR.index(min(agingR))
    print(f"Selecting frame {frameToReplace} for replacement based on aging.")
    return frameToReplace

def updateAgingBuffer(agingR, frames, decoder):
    for i in range(len(agingR)):
        agingR[i] >>= 1
        if decoder.getReferenced(frames[i]):
            agingR[i] |= (1 << 7)
            frames[i] = decoder.clearReferenced(frames[i])

def main(filename):
    virBits, phyBits, pageBits, numProcesses, memAccesses = readFile(filename)

    virMemSize = 2 ** virBits
    phyMemSize = 2 ** phyBits
    pageSize = 2 ** pageBits

    print("INITIAL PAGETABLE SETUP:")
    print("  Virtual Memory Size:", virMemSize)
    print("  Physical Memory Size:", phyMemSize)
    print("  Page Size:", pageSize)    

    numPages = 2 ** (virBits - pageBits)
    numFrames = 2 ** (phyBits - pageBits)
    processBits = math.ceil(math.log2(numProcesses))

    print("  Number of Pages:", numPages)
    print("  Number of Frames:", numFrames)
    print("  FrameBits:", math.ceil(math.log2(numFrames)))
    print("  Number of Processes:", numProcesses)

    decoder = InvertedPageTableDecoder(processBits, pageBits)

    frames = [0] * numFrames
    pageLookup = {}
    freeFrames = list(range(numFrames))

    print("Free Frames: ", freeFrames)

    pageTables = []
    for i in range(numProcesses):
        pageTables.append([0] * numPages)
    print("Page Tables: ", pageTables)

    agingBits = 8
    agingR = [0] * numFrames
    numInstructions = 0

    displayInvertedPageTable(frames, decoder, agingR)

    frameNum = -1

    for memAccess in memAccesses:
        print("-----------------------------------------------------------")
        numInstructions += 1

        parts = memAccess.split()
        processNum = int(parts[0])
        command = parts[1]  # 'r' or 'w'
        virMemLoc = int(parts[2])

        print("Process:", processNum, " Command:", command, " Virtual Memory Location:", virMemLoc)

        pageNum = virMemLoc >> pageBits
        offset = virMemLoc & ((1 << pageBits) - 1)

        print("  pageNum: ", pageNum, "  offset: ", offset)

        # Ensure page lookup is updated properly to avoid page faults
        frameNum = pageLookup.get((processNum, pageNum), -1)
        if frameNum != -1:
            present = True
        else:
            present = decoder.getPresent(pageTables[processNum][pageNum])

        if present:
            if frameNum == -1:
                frameNum = pageLookup.get((processNum, pageNum), -1)  # Correctly set frameNum
            frames[frameNum] = decoder.setReferenced(frames[frameNum])
            if command == 'w':
                frames[frameNum] = decoder.setModified(frames[frameNum])
        else:
            print(" *** Page Fault ***")

            if len(freeFrames) > 0:
                frameNum = freeFrames.pop(0)
            else:
                frameNum = selectReplacementFrame(agingR)
                
                oldProc = decoder.getProcess(frames[frameNum])
                oldPage = decoder.getPage(frames[frameNum])

                print(f"    Removing page {oldPage} of process {oldProc} from frame {frameNum}.")

                if (oldProc, oldPage) in pageLookup:
                    del pageLookup[(oldProc, oldPage)]

                frames[frameNum] = 0 

            frames[frameNum] = decoder.replaceProcessAndPage(frames[frameNum], processNum, pageNum)
            frames[frameNum] = decoder.setPresent(frames[frameNum])
            pageLookup[(processNum, pageNum)] = frameNum

            agingR[frameNum] = (1 << 8) - 1  # Reset aging register
            print(f"    Loading page {pageNum} of process {processNum} into frame {frameNum}.")
        
        print(f"Frame number: {frameNum}, Page size: {pageBits}, Offset: {offset}")
        phyMemLoc = (frameNum << pageBits) | offset
        print(f"--> Physical Location: {phyMemLoc}")

        # update the reference bit after calculating the physical location
        frames[frameNum] = decoder.setReferenced(frames[frameNum])

        if command == 'w':
            frames[frameNum] = decoder.setModified(frames[frameNum])

        if numInstructions % 3 == 0:
            print(" ***Aging Buffer Update***")
            updateAgingBuffer(agingR, frames, decoder)

        # # Now clear the frame (if it was replaced) after aging and reference updates
        # if len(freeFrames) == 0 and frameNum not in freeFrames:
        #     frames[frameNum] = 0

        displayInvertedPageTable(frames, decoder, agingR)

if __name__ == "__main__":
    #main("testCases/inputOne.txt")
    main("testCases/inputTwo.txt")
