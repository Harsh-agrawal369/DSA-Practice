class Solution:
    def findMissingAndRepeatedValues(self, grid: List[List[int]]) -> List[int]:
        len_arr = len(grid)
        
        dup, miss = None, None

        temp = [True]*(len_arr*len_arr)

        for i in grid:
            for j in i:
                if temp[j-1] == False:
                    dup = j
                else: temp[j-1] = False

        miss = temp.index(True) + 1

        return [dup, miss]