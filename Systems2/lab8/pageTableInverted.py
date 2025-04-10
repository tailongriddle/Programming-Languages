import math

# Inverted Page Table Decoder
# This will decode the entries of the inverted page table which stores Process# and Page#
class PageTableDecoder:
    def __init__(self, processBits, pageBits):
        self.processBits = processBits # add process bits
        self.pageBits = pageBits # add page bits

    def getModified(self, pageTableEntry):
        return (pageTableEntry >> (self.processBits + self.pageBits + 2)) & 1
    
    def getReferenced(self, pageTableEntry):
        return (pageTableEntry >> (self.processBits + self.pageBits + 1)) & 1
    
    def getPresent(self, pageTableEntry):
        return (pageTableEntry >> (self.processBits + self.pageBits)) & 1
    
    def setModified(self, pageTableEntry):
        return pageTableEntry | (1 << (self.processBits + self.pageBits + 2))
    
    def setReferenced(self, pageTableEntry):
        return pageTableEntry | (1 << (self.processBits + self.pageBits + 1))
    
    def setPresent(self, pageTableEntry):
        return pageTableEntry | (1 << (self.processBits + self.pageBits))
    
    def clearModified(self, pageTableEntry):
        return pageTableEntry & ~(1 << (self.processBits + self.pageBits + 2))
    
    def clearReferenced(self, pageTableEntry):
        return pageTableEntry & ~(1 << (self.processBits + self.pageBits + 1))
    
    def clearPresent(self, pageTableEntry):
        return pageTableEntry & ~(1 << (self.processBits + self.pageBits))
    
    # Get the process number and page number from the entry
    def getProcessNum(self, pageTableEntry):
        return (pageTableEntry >> self.pageBits) & ((1 << self.processBits) - 1)
    
    def getPageNum(self, pageTableEntry):
        return pageTableEntry & ((1 << self.pageBits) - 1)
    
    # Replace process and page number in the entry
    def replaceProcessPage(self, pageTableEntry, processNum, pageNum):
        # First clear the old process and page bits
        temp = pageTableEntry & ~(((1 << self.processBits) - 1) << self.pageBits)
        # Then set the new process and page number
        return temp | (processNum << self.pageBits) | pageNum


# function to select frame to replace based on aging replacement policy
def selectReplacementFrame(agingR):
    frameToReplace = agingR.index(min(agingR)) # select the frame with the lowest aging value
    print(f"Selecting frame {frameToReplace} for replacement based on aging.")
    return frameToReplace

# function to update  aging buffer
def updateAgingBuffer(agingR, frames, decoder):
    for i in range(len(agingR)):
        agingR[i] >>= 1 # shift all bits to the right
        if decoder.getReferenced(frames[i]):
            agingR[i] |= (1 << 7) # set the leftmost bit
            frames[i] = decoder.clearReferenced(frames[i])

# function to display  inverted page table and aging status
def displayPageTable(frames, decoder, agingR):
    print("\nInverted Page Tables (with associated aging status):")
    print("frame#\tmod\tref\tpresent\tprocess#\tpage#\taging")
    for frameNum, aging in enumerate(agingR): # iterate through the frames
        isFound = False # flag to check if the frame is found
        pageTableEntry = frames[frameNum]

        if decoder.getPresent(pageTableEntry): # if the frame is present in the page table...
            prn = decoder.getProcessNum(pageTableEntry)
            pn = decoder.getPageNum(pageTableEntry)
            m = decoder.getModified(pageTableEntry)
            r = decoder.getReferenced(pageTableEntry)
            p = decoder.getPresent(pageTableEntry)

            isFound = True # set the flag to true
            print(f"{frameNum}\t{m}\t{r}\t{p}\t{prn}\t{pn}\t{aging}")
        if not isFound: # if the frame is not found in the page table...
            print(f"{frameNum}\t-\t-\t-\t-\t-\t-")

# function to read input file
def readFile(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    virBits = int(lines[0].split()[0])
    phyBits = int(lines[0].split()[1])
    pageBits = int(lines[0].split()[2])
    numProcesses = int(lines[1])

    lines = lines[2:]

    return virBits, phyBits, pageBits, numProcesses, lines

def main(filename):
    virBits, phyBits, pageBits, numProcesses, memAccesses = readFile(filename) # read the input file

    virMemSize = 2 ** virBits
    phyMemSize = 2 ** phyBits
    pageSize = 2 ** pageBits

    print("INITIAL PAGETABLE SETUP:")
    print("  Virtual Memory Size:", virMemSize)
    print("  Physical Memory Size:", phyMemSize)
    print("  Page Size:", pageSize)

    # calculate the number of pages and frames
    numPages = 2 ** (virBits - pageBits) 
    numFrames = 2 ** (phyBits - pageBits)
    processBits = int(math.log2(numProcesses))

    # create a page table decoder
    decoder = PageTableDecoder(processBits, pageBits)

    print("  Number of Pages:", numPages)
    print("  Number of Frames:", numFrames)
    print("  Number of processes:", numProcesses)
    print("  Frame Bits:", processBits)

    frames = [0] * numFrames
    pageLookup = {} # Store (processNum, pageNum) -> frameNum
    freeFrames = list(range(numFrames))

    agingBits = 8  # number of bits used for aging
    agingR = [0] * numFrames  # aging buffer to track the age of each frame
    numInstructions = 0  # counter for the number of instructions

    displayPageTable(frames, decoder, agingR)

    for memAccess in memAccesses:
        print("-----------------------------------------------------------")
        numInstructions += 1 # increment the num of instructions

        processNum, command, virMemLoc = memAccess.split()
        print("Process:", processNum, " Command:", command, " Virtual Memory Location:", virMemLoc)

        processNum = int(processNum)
        virMemLoc = int(virMemLoc)
        pageNum = virMemLoc >> pageBits
        offset = virMemLoc & ((1 << pageBits) - 1)

        print("  pageNum: ", pageNum, "  offset: ", offset)
        # check if the page is in the page table
        frameNum = -1
        for i in range(numFrames):
            if decoder.getPresent(frames[i]) and decoder.getProcessNum(frames[i]) == processNum and decoder.getPageNum(frames[i]) == pageNum:
                frameNum = i
                break
        # if the page is in the page table...
        if frameNum != -1:
            frames[frameNum] = decoder.setReferenced(frames[frameNum])
            if command == 'w':
                frames[frameNum] = decoder.setModified(frames[frameNum])
        else: # if the page is not in the page table...
            print(" *** Page Fault ***")

            if len(freeFrames) > 0: # if there are free frames...
                frameNum = freeFrames.pop(0)
            else: # if there are no free frames...
                frameNum = selectReplacementFrame(agingR)

                oldProc = decoder.getProcessNum(frames[frameNum])
                oldPage = decoder.getPageNum(frames[frameNum])

                print(f"    Removing page {oldPage} of process {oldProc} from frame {frameNum}.")

                if (oldProc, oldPage) in pageLookup: # remove the old page from the page lookup
                    del pageLookup[(oldProc, oldPage)]

                frames[frameNum] = 0
            # load the new page into the frame
            frames[frameNum] = decoder.replaceProcessPage(frames[frameNum], processNum, pageNum)
            frames[frameNum] = decoder.setPresent(frames[frameNum])
            pageLookup[(processNum, pageNum)] = frameNum
            # set the aging value of the frame to maximum value
            agingR[frameNum] = (1 << 8) - 1
            print(f"    Loading page {pageNum} of process {processNum} into frame {frameNum}.")

        updateAgingBuffer(agingR, frames, decoder) # update aging buffer
        displayPageTable(frames, decoder, agingR) # display page table

if __name__ == "__main__":
    main("testCases/inputTwo.txt")
