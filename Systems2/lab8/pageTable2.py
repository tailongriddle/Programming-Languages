import math

# PageTableDecoder class to handle bit manipulations in the page table entries
class PageTableDecoder:
    def __init__(self, processBits, pageBits):
        self.processBits = processBits
        self.pageBits = pageBits

    def getModified(self, pageTableEntry):
        return (pageTableEntry >> (self.processBits + self.pageBits + 2)) & 1

    def getReferenced(self, pageTableEntry):
        return (pageTableEntry >> (self.processBits + self.pageBits + 1)) & 1

    def getPresent(self, pageTableEntry):
        return (pageTableEntry >> (self.processBits + self.pageBits)) & 1

    def getProcess(self, pageTableEntry):
        return (pageTableEntry >> self.pageBits) & ((1 << self.processBits) - 1)

    def getPage(self, pageTableEntry):
        return pageTableEntry & ((1 << self.pageBits) - 1)

    def setModified(self, pageTableEntry):
        return pageTableEntry | (1 << (self.processBits + self.pageBits + 2))

    def setReferenced(self, pageTableEntry):
        return pageTableEntry | (1 << (self.processBits + self.pageBits + 1))

    def setPresent(self, pageTableEntry):
        return pageTableEntry | (1 << (self.processBits + self.pageBits))

    def replaceProcessPage(self, pageTableEntry, processNum, pageNum):
        # First clear the process and page bits, then set new values
        temp = pageTableEntry & ~(((1 << self.processBits) - 1) << self.pageBits)
        return temp | (processNum << self.pageBits) | pageNum


# Initialize the inverted page table with all frames empty
def initializeInvertedPageTable(numFrames, processBits, pageBits):
    return [0] * numFrames  # Each frame starts with the value 0, indicating no page loaded.


# Find the page in the inverted page table
def findPageInInvertedTable(invertedPageTable, processNum, pageNum, decoder):
    for frameNum in range(len(invertedPageTable)):
        entry = invertedPageTable[frameNum]
        if decoder.getPresent(entry) and decoder.getProcess(entry) == processNum and decoder.getPage(entry) == pageNum:
            return frameNum  # Page is loaded in this frame
    return -1  # Page not found in any frame


# Replace a page using the aging algorithm
def replacePageInFrame(invertedPageTable, agingR, numFrames, decoder, processNum, pageNum):
    # Find the oldest page to replace using the aging algorithm
    oldestAge = max(agingR)
    oldestFrame = agingR.index(oldestAge)

    # Check if the page in the oldest frame is modified and needs to be written back
    oldModified = decoder.getModified(invertedPageTable[oldestFrame])
    if oldModified:
        print(f"    Writing modified data from frame {oldestFrame}...")

    # Remove the old page from the frame
    invertedPageTable[oldestFrame] = 0
    agingR[oldestFrame] = 0  # Reset the aging for the replaced frame

    # Load the new page into the selected frame
    invertedPageTable[oldestFrame] = decoder.replaceProcessPage(invertedPageTable[oldestFrame], processNum, pageNum)
    agingR[oldestFrame] = (1 << 8) - 1  # Set the new page's age to the maximum (freshly loaded)
    print(f"    Loading page {pageNum} of process {processNum} to frame {oldestFrame}")

    return oldestFrame


# Display the state of the inverted page table and aging buffer
def displayPageTable(invertedPageTable, decoder, agingR):
    print("Inverted Page Table:")
    for frameNum, entry in enumerate(invertedPageTable):
        if entry == 0:
            print(f" Frame {frameNum}: Empty")
        else:
            processNum = decoder.getProcess(entry)
            pageNum = decoder.getPage(entry)
            print(f" Frame {frameNum}: Process {processNum} Page {pageNum}")
    print("Aging Buffer:", agingR)


# Main function to simulate memory access using an inverted page table
def main(filename):
    # Read the input file and extract memory configuration details
    virBits, phyBits, pageBits, numProcesses, memAccesses = readFile(filename)

    virMemSize = 2 ** virBits
    phyMemSize = 2 ** phyBits
    pageSize = 2 ** pageBits

    numFrames = phyMemSize // pageSize
    numPages = virMemSize // pageSize
    processBits = int(math.log2(numProcesses))

    decoder = PageTableDecoder(processBits, pageBits)

    invertedPageTable = initializeInvertedPageTable(numFrames, processBits, pageBits)
    agingR = [0] * numFrames
    freeFrames = [i for i in range(numFrames)]

    numInstructions = 0
    for memAccess in memAccesses:
        print("-----------------------------------------------------------")
        numInstructions += 1

        processNum, command, virMemLoc = memAccess.split()
        processNum = int(processNum)
        virMemLoc = int(virMemLoc)
        pageNum = virMemLoc >> pageBits
        offset = virMemLoc & (pageSize - 1)

        print(f"Process: {processNum}, Command: {command}, Virtual Memory Location: {virMemLoc}")
        print(f"  pageNum: {pageNum}, offset: {offset}")

        # Find the frame containing the requested page
        frameNum = findPageInInvertedTable(invertedPageTable, processNum, pageNum, decoder)

        if frameNum == -1:
            print(" *** Page Fault ***")
            # No free frame, replace one using aging
            if len(freeFrames) > 0:
                frameNum = freeFrames.pop(0)
                invertedPageTable[frameNum] = decoder.replaceProcessPage(invertedPageTable[frameNum], processNum, pageNum)
                agingR[frameNum] = (1 << 8) - 1  # Set the new page's age to maximum
            else:
                frameNum = replacePageInFrame(invertedPageTable, agingR, numFrames, decoder, processNum, pageNum)

        # Physical memory location is calculated as before
        phyMemLoc = (frameNum << pageBits) | offset
        print(f"--> Physical Location: {phyMemLoc}")

        # Update the page table entry reference bit
        invertedPageTable[frameNum] = decoder.setReferenced(invertedPageTable[frameNum])

        if command == 'w':
            invertedPageTable[frameNum] = decoder.setModified(invertedPageTable[frameNum])

        # Update the aging buffer
        if numInstructions % 3 == 0:
            print(" *** Aging Buffer Update ***")
            for i in range(numFrames):
                agingR[i] = agingR[i] >> 1
                # Transfer the R bit from the inverted page table entry
                if decoder.getReferenced(invertedPageTable[i]) == 1:
                    agingR[i] |= (1 << 7)
                invertedPageTable[i] = decoder.setReferenced(invertedPageTable[i])

        # Display the page table and aging buffer
        displayPageTable(invertedPageTable, decoder, agingR)


# Read the input file and parse the memory configuration and memory accesses
def readFile(filename):
    with open(filename, 'r') as f:
        virBits, phyBits, pageBits, numProcesses = map(int, f.readline().split())
        memAccesses = [line.strip() for line in f.readlines()]
    return virBits, phyBits, pageBits, numProcesses, memAccesses


# Run the simulation with the specified input file
if __name__ == "__main__":
    filename = "testCases/input.txt"  # Replace with the actual file path if needed
    main(filename)
