import inspect
import io
import os
import sys
import shutil
from io import BytesIO
from pathlib import Path
from typing import Any
from PIL import Image
from pixelmatch.contrib.PIL import pixelmatch
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from playwright.sync_api import Page, Locator
import allure
from allure_commons.types import AttachmentType

class VisualTestMain:

    def __init__(self, snapshot_path:str='', driverpage:Any='', updatesnapshot=False, savefailuresnapondisk=True, allurereport=False):
        if type(driverpage)==webdriver.Chrome or type(driverpage)==webdriver.Edge or type(driverpage)==webdriver.Firefox or type(driverpage)==webdriver.Ie:
            self.driver = driverpage
            self.isSelenium = True
        elif type(driverpage)==Page:
            self.page = driverpage
            self.isSelenium = False
        self.snapshot_path = snapshot_path
        self.updatesnapshots = updatesnapshot
        #======================For reporting=========================
        self.allurereport = allurereport
        self.golden_snapshot = ''
        self.golden_snapshot_name = ''
        self.expected_snapshot = ''
        self.expected_snapshot_name = ''
        self.diff_snapshot = ''
        self.diff_snapshot_name = ''
        self.savefailuresnapondisk = savefailuresnapondisk
        self.numberofclassesaftertestclass = 0
        #============================================================
        
    def setpaths(self, updatesnapshot=False, numberofclassesaftertestclass:int=0) -> None:
        self.numberofclassesaftertestclass = numberofclassesaftertestclass
        self.total_result = True #For accumulating the results of all the tests for the current session
        self.test_func_name = self.retrieve_function_name()
        self.test_name = f"{str(sys.platform)}_{self.test_func_name}"
        self.test_dir = self.test_func_name
        classname = self.retrieve_class_name()
        self.test_file_name = classname.split(os.sep)[-1].strip('.py') #classname.split('\\')[-1].strip('.py')
        self.resultpath = str(Path(classname).parent.resolve()) if self.snapshot_path == '' else self.snapshot_path
        self.base_path = self.resultpath + os.sep + "Golden_Snapshots" + os.sep +  self.test_file_name +  os.sep + self.test_dir
        self.filepath = Path(self.base_path).absolute().resolve()
        # Create a dir where all snapshot test failures will go
        self.results_dir_name_str = self.resultpath + os.sep +  "Failure_Snapshots" + os.sep +  self.test_file_name  + os.sep + self.test_name
        self.test_results_dir = Path(self.results_dir_name_str).absolute().resolve()
        # Remove a single test's past run dir with actual, diff and expected images
        if self.test_results_dir.exists():
            shutil.rmtree(self.test_results_dir)
        if updatesnapshot == True:
            self.updatesnapshots = True

    def captureGoldenSnapshot(self, img: bytes, *, stepname = '') -> bool:
        try:
            self.filepath.mkdir(parents=True, exist_ok=True)
            name = f'{self.test_name}.png' if stepname == '' else f'{self.test_name}_{stepname}.png'
            file = self.filepath / name
            if not file.exists():
                print("--> Golden snapshots will be created. Please review images")
            file.write_bytes(img)
            print("--> Golden snapshots updated. Please review images")
            self.golden_snapshot = img # For reporting purpose
            self.golden_snapshot_name = name # For reporting purpose
        except Exception as e:
            print("Error occurred while capturing Golden Snapshot")
            print(e)
            return False
        else:
            return True

    def compareSnapshots(self, img: bytes, *, stepname = '', threshold: float = 0.1, fail_fast=False) -> bool:
        try:
            name = f'{self.test_name}.png' if stepname == '' else f'{self.test_name}_{stepname}.png'
            file = self.filepath / name
            if not file.exists():
                self.filepath.mkdir(parents=True, exist_ok=True)
                file.write_bytes(img)
                print("--> Golden snapshots not found, so new Golden snapshot(s) created. Please review images and execute the tests again.")
                self.golden_snapshot = img # For reporting purpose
                self.golden_snapshot_name = name # For reporting purpose
                return False
            else:
                img_a = Image.open(BytesIO(img))
                img_b = Image.open(file)
                img_diff = Image.new("RGBA", img_a.size)
                try:
                    mismatch = pixelmatch(img_a, img_b, img_diff, threshold=threshold, fail_fast=fail_fast)
                    if mismatch == 0:
                        print("--> Snapshots match perfectly!")
                        return True
                    else:
                        match = False
                except Exception as e:
                    print("Image sizes did not match!!!")
                    print(e)
                    match = False
                if not match:
                    #======================For reporting=========================
                    self.golden_snapshot = img
                    self.golden_snapshot_name = f'Golden_{name}'

                    #self.expected_snapshot = img_b.tobytes("hex", "rgb")
                    img_b_byte_arr = io.BytesIO()
                    img_b.save(img_b_byte_arr, format='PNG')
                    img_b_byte_arr = img_b_byte_arr.getvalue()
                    self.expected_snapshot = img_b_byte_arr
                    self.expected_snapshot_name = f'Actual_{name}'

                    #self.diff_snapshot = img_diff.tobytes("hex", "rgb")
                    img_diff_byte_arr = io.BytesIO()
                    img_diff.save(img_diff_byte_arr, format='PNG')
                    img_diff_byte_arr = img_diff_byte_arr.getvalue()
                    self.diff_snapshot = img_diff_byte_arr
                    self.diff_snapshot_name = f'Diff_{name}'
                    #==========================To save snaps on disk==================================
                    if self.savefailuresnapondisk:
                        # Create new test_results folder
                        self.test_results_dir.mkdir(parents=True, exist_ok=True)
                        img_a.save(f'{self.test_results_dir}/{self.golden_snapshot_name}')
                        img_b.save(f'{self.test_results_dir}/{self.expected_snapshot_name}')
                        img_diff.save(f'{self.test_results_dir}/{self.diff_snapshot_name}')
                    #============================================================
                    if self.allurereport:
                        allure.attach(self.golden_snapshot, name=self.golden_snapshot_name, attachment_type=AttachmentType.PNG)
                        allure.attach(self.expected_snapshot, name=self.expected_snapshot_name, attachment_type=AttachmentType.PNG)
                        allure.attach(self.diff_snapshot, name=self.diff_snapshot_name, attachment_type=AttachmentType.PNG)
                    print("--> Snapshots DO NOT match!")
                    return False
        except Exception as e:
            print("Exception occurred during snapshot comparison:")
            print(e)
            return False
        

    def visualtest_web(self, *, stepname = '', threshold: float = 0.1, 
                   fail_fast=False, updatesnapshot=False, fullpage = True, snapshot_of_locators:list=[],
                   exclude_locators:list=[], numberofclassesaftertestclass:int=0) -> bool:
        if self.updatesnapshots == True:
            updatesnaps = self.updatesnapshots
        else:
            updatesnaps = updatesnapshot
        result = True
        if len(snapshot_of_locators) > 0:
            for element in snapshot_of_locators:
                if type(element) == WebElement:
                    img = element.screenshot_as_png
                elif type(element) == Locator:
                    img = element.screenshot()
                result = result & self.visualtest(img=img, stepname=stepname+str(self.retrieve_variable_name(element, numberofclassesaftertestclass)), 
                                threshold=threshold, fail_fast=fail_fast,
                                 updatesnapshot=updatesnaps)
        else:
            if self.isSelenium:
                img = self.driver.get_screenshot_as_png()
            else:
                img = self.page.screenshot(full_page=fullpage)
            result = self.visualtest(img=img, stepname=stepname, 
                                threshold=threshold, fail_fast=fail_fast,
                                 updatesnapshot=updatesnaps)
        return result


    def visualtest(self, img: bytes, *, stepname = '', threshold: float = 0.1, 
                   fail_fast=False, updatesnapshot=False) -> bool:
        if updatesnapshot == True:
            return self.captureGoldenSnapshot(img=img, stepname=stepname)
        else:
            return self.compareSnapshots(img=img, stepname=stepname, threshold=threshold, fail_fast=fail_fast)

    #Auxiliary method for retrieving variable names
    def retrieve_variable_name(self, var, numberofclassesaftertestclass:int=0):
        basicframename = inspect.currentframe().f_back.f_back.f_back
        for i in range(numberofclassesaftertestclass):
            basicframename = basicframename.f_back
        callers_local_vars = basicframename.f_locals.items()
        return [var_name for var_name, var_val in callers_local_vars if var_val is var]
    
    #Auxiliary method for retrieving calling function's names
    def retrieve_function_name(self):
        basicfuncname = inspect.currentframe().f_back.f_back.f_back
        for i in range(self.numberofclassesaftertestclass):
            basicfuncname = basicfuncname.f_back
        return basicfuncname.f_code.co_name
    
    #Auxiliary method for retrieving calling class's names
    def retrieve_class_name(self):
        basicclassname = inspect.currentframe().f_back.f_back.f_back
        for i in range(self.numberofclassesaftertestclass):
            basicclassname = basicclassname.f_back
        return basicclassname.f_code.co_filename