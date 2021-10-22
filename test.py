def change(dic):
	dic["why"] = "x";
	print(dic)
	return dic
dic = {}
dic["no"] = "n"
change(dic)
print(dic)