* Having many copies of the same schedule.
* Transpose coord and schedule so that assignments are faster.
* self.cursor = coords.shape[1] - 1 is potentially a problem (as the numbers goes down, harder to extend)
* Generating path should be vectorized
* the order of time vs coord in functions signature
* 