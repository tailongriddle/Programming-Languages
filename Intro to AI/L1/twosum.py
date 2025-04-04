
def twoSum(nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        diff_map = {}
        num_map = {}
        
        for i_index, i in enumerate(nums):
            diff = target - i
            diff_map[diff] = i
            num_map[i] = i_index
        
        print(list(diff_map))  
        print(list(num_map))   
            
        for j_index, j in enumerate(nums):
            if j in diff_map and j_index != num_map.get(diff_map.get(j)): # if j in diff map
                print(j_index,num_map.get(diff_map.get(j)))
                return j_index,num_map.get(diff_map.get(j))
                          
            
twoSum([3,2,4],6)