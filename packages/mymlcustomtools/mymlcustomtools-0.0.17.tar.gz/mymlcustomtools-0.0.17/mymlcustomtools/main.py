import time
import inspect
import os
import sys
import pickle
from sklearn.model_selection import GridSearchCV

__fit_model_counter = 0
def save(model,silent=False):
	"""
	Saves the model in a predefined directory. This function is automatically called by fit,
	so that the model isn't lost by accident after spending hours training
	"""
	global __fit_model_counter, DIR_PATH

	if DIR_PATH is None:
		return

	existing_models = [fn[:-6] for fn in os.listdir(DIR_PATH) if fn[-6:]==".model"]
	__fit_model_counter = 1 + max(__fit_model_counter, *[int(model_name) if model_name.isnumeric() else 0 for model_name in existing_models], -1)

	filepath = os.path.join(DIR_PATH, f"{__fit_model_counter}.model")
	with open(filepath, "wb") as f:
		if not silent: print(f"Saving {filepath}...")
		pickle.dump(model, f)

__mounted = False
def mount(dirpath,silent=False):
	"""
	If executed inside a Google Colab notebook, this function mounts the Google Drive storage
	so that the model is saved there permantently. Otherwise, it tries to locate the directory
	where the program is being executed.
	"""
	global DIR_PATH, __mounted
	if __mounted: return
	__mounted = True

	if dirpath is not None:
		DIR_PATH = dirpath
		return

	try:
		from google.colab import drive
		drive.mount('/content/drive')
		DIR_PATH = "/content/drive/MyDrive/Colab Notebooks/output"
		if not silent: print("Mounted Google Drive folder successfully")
	except:
		try:
			DIR_PATH = os.path.dirname(os.path.abspath(inspect.currentframe().f_back.f_back.f_globals.get('__file__', None)))
			if not silent: print(f"Saving locally in directory {DIR_PATH}")
		except:
			DIR_PATH = None
			if not silent: print("Couldn't find a directory to save. Not saving the model")

def bar_fit(model, X, y):
	"""
	This function creates a loading bar to GridSearchCV by capturing the stdout during training
	"""
	__is_notebook = False
	try:
		__is_notebook = get_ipython().__class__.__name__ in ["ZMQInteractiveShell","Shell"]
	except: pass
	if __is_notebook:
		from tqdm.notebook import tqdm
	else:
		from tqdm import tqdm

	class BarStdout:
		def write(self, text):
			if "totalling" in text and "fits" in text:
				self.bar_size = int(text.split("totalling")[1].split("fits")[0][1:-1])
				self.bar = tqdm(total=self.bar_size)

				self.count = 0
				return
			if "CV" in text and hasattr(self,"bar"):
				self.count += 1
				self.bar.update(n=self.count-self.bar.n)
				if self.count%(self.bar_size//10)==0:
					time.sleep(0.1)
		def flush(self, text=None):
			pass
	default_stdout= sys.stdout
	sys.stdout = BarStdout()
	model.verbose = 5
	model.fit(X, y)
	sys.stdout = default_stdout

def fit(model, X, y, silent=False, dirpath=None):
	"""
	This function is ment to substitute the model.fit method. Although it calls it internally, it also
	executes other functions, such as measuring the time taken, automatically saving the model, and
	adding a loading bar to GridSearchCV fit call. For more information about the saved models, execute
	load_models(), or try help(save).
	"""
	mount(dirpath,silent=silent)

	initial_time = time.time()
	if type(model)==GridSearchCV:
		bar_fit(model, X, y)
	else:
		model.fit(X, y)
	final_time   = time.time()
	elapsed_time = final_time - initial_time
	if not silent: print("Elapsed time: " + ("{:.1f} s".format(elapsed_time)) if elapsed_time < 60 else ("{:.0f} min {:.0f} s".format(round(elapsed_time,0)//60,round(elapsed_time,0)%60)) )

	save(model,silent=silent)
	return model
	
def load_models(model_number=None):
	"""
	This function loads the saved models after fitting. Executing load_models() informs the files saved
	and their directory. To get the saved model, just inform its number as an integer.
	"""
	mount()
	existing_models = [fn[:-6] for fn in os.listdir(DIR_PATH) if fn[-6:]==".model"]

	if model_number is None:
		if existing_models:
			print("Existing models:\n"+"\n".join([model_name+".model" for model_name in existing_models]))
		else:
			print("No model saved")
		return

	model_number = model_number if type(model_number)==int else int(model_number.replace(".model",""))
	filepath = os.path.join(DIR_PATH, f"{model_number}.model")
	with open(filepath, "rb") as f:
		print(f"Loading {filepath}...")
		model = pickle.load(f)

	return model