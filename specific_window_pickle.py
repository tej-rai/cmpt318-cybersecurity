import pickle
import pandas as pd

SQUASH_SIZE = 1

def dump(variable, fileName):
	with open(fileName+".pickle", 'wb') as handle:
		print("var: ", len(variable), "\t\tfileName: ", fileName)
		pickle.dump(variable, handle, protocol=pickle.HIGHEST_PROTOCOL)

def summer_winter(fileName):
	with open(fileName+'.pickle', 'rb') as handle:
		df = pickle.load(handle)
	df = df.dropna()
	s = df[(df.d.dt.month > 3) & (df.d.dt.month < 10)]
	w = df[(df.d.dt.month <= 3) | (df.d.dt.month >= 10)]

	summer = split(s)
	winter = split(w)

	def dump_split(name, x):
		dump(x[0][0], fileName+"-"+name+"-day-weekday")
		dump(x[0][1], fileName+"-"+name+"-day-weekend")
		dump(x[1][0], fileName+"-"+name+"-night-weekday")
		dump(x[1][1], fileName+"-"+name+"-night-weekend")

	dump_split("summer", summer)
	dump_split("winter", winter)


def split(s):
	offset = pd.DateOffset(hours=6)
	s.d -= offset
	day = s[s.d.dt.hour < 12]
	night = s[s.d.dt.hour >= 12]

	def week_split(x, weekend_start):
		weekend = x[x.d.dt.weekday >= weekend_start]
		weekday = x[x.d.dt.weekday < weekend_start]

		def convert(q):
			arr = []
			group = q.groupby((q.d.dt.year, q.d.dt.month, q.d.dt.day))
			max_val = 720
			# max_val = group.count().max().values.max()
			for g in group:
				a = g[1]
				values = a.count().values
				if values.min() != max_val and values.max() != max_val:
					continue
				a.d += offset
				# a = a.set_index(['d'])
				# a['m']= a.d.dt.hour*(60//SQUASH_SIZE) + a.d.dt.minute//SQUASH_SIZE
				# a = a.groupby(a.m).mean().reset_index()
				arr.append(a)
			return arr
		return [convert(weekday), convert(weekend)]

		# return [weekday, weekend]

	day_split = week_split(day, weekend_start=5)
	night_split = week_split(night, weekend_start=4)

	return [day_split, night_split]

# summer_winter("train")
# summer_winter("test")
summer_winter("test2")