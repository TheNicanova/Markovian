* Having many copies of the same schedule.
* Transpose coord and schedule so that assignments are faster.
d* self.cursor = coords.shape[1] - 1 is potentially a problem (as the numbers goes down, harer to extend)
* Generating path should be vectorized
* the order of time vs coord in functions signature
* Add a check to see whether all point are the same.
* Must track what relies on numpy broadcasting (e.g. lambda expression)
* Cursor change name to teleporter?