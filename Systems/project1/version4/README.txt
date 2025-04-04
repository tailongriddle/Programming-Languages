Partners: Tai-Long Riddle and Christy Vo
How far we got: Mostly through version 4
Why we got stuck:

The logic in both the minor and major collections in version 4 seem mostly sound. 
There are two issues. For one, there is a memory leak somewhere in the code.
We cannot seem to figure out where exactly this is happening and why.
This is only evident because of the memory dumps. When printing out the survival amount for the largest free blocks in the last few function calls, the amount randomly becomes a very large number that is different every single time the code is run. 
The variance in the number makes us suspect that this is a memory leak. The other issue is the memory call at the end of version four. After running several extra memory call functions, we determined that it is after the third call of the minor collection that the call to a1 is corrupted in some sense. 
Before that, the previous two memory calls output "Denver". After, they output nothing. The memory dumps are consistent with where the memory should be, so we are unsure as to where and why this issue occurs. 
