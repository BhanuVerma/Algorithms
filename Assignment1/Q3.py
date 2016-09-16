class Tag(object):
	def __init__(self, val):
		self.val = val


class Solution(object):
	def determineMajority(self, tagList):
		if len(tagList) == 1:
			return tagList[0]

		left = self.determineMajority(tagList[0:int(len(tagList)/2)])
		right = self.determineMajority(tagList[int(len(tagList)/2):len(tagList)])

		if left and right:
			if left.val == right.val:
				return left
			else:
				majority = self.getMajority(left,right,tagList)
				return majority
		else:
			majority = self.getMajority(left,right,tagList)
			return majority
			

	def getMajority(self,left,right,union):
		left_count = 0
		right_count = 0
		for tag in union:
			if left and left.val == tag.val:
				left_count += 1
			elif right and right.val == tag.val:
				right_count += 1
			else:
				pass

		if left_count > right_count and left_count > len(union)/2:
			return left
		elif right_count > left_count and right_count > len(union)/2:
			return right
		else:
			return None


tagArr = [0,0,0,0,0,0,0,1,1,1,1,1,1,1]
tag_list = []
for tag_id in tagArr:
	tag = Tag(tag_id)
	tag_list.append(Tag(tag_id))

sol = Solution()
majority = sol.determineMajority(tag_list)
if majority:
	print(majority.val)
else:
	print("No Majority")