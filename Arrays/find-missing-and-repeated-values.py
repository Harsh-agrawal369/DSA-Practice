# Naive solution flag based

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
    
    
# Mathematical Solution
def findMissingAndRepeatedValues(self, grid: List[List[int]]) -> List[int]:

        n = len(grid)
        sz = n*n

        # sum(grid) 
        sum_grid = sum(num for row in grid for num in row)
        # what should be ideal sum
        ideal_sum = sz * (sz+1)//2

        # Repeat - missing = sum of grid - ideal sum
        diff_sum = sum_grid - ideal_sum


        # Sum(sq)
        sum_sq_grid = sum(num*num for row in grid for num in row)
        # Ideal Sum of sq
        sum_sq_ideal = sz * (sz+1) *  (2*sz + 1) // 6

        # Repeat^2 - Ideal^2
        diff_sq = sum_sq_grid - sum_sq_ideal

        # a^2 - b^2 = (a-b) * (a+b) we have (a-b) and a^2 - b^2
        # Hence (a+b) = (a^2 - b^2)//(a-b)

        #sum of repeat + missing
        sum_rp_ms = diff_sq//diff_sum

        repeat = (sum_rp_ms + diff_sum) // 2
        missing = (sum_rp_ms - diff_sum) // 2

        return [repeat, missing]