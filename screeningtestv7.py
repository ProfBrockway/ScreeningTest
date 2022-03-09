
r"""
# To run the web browser and see our web page enter the following command.
# streamlit run "G:\My Drive\UConn\1-Subjects\Python\STAT476\CODE\ScreeningTest\screeningtestv7.py"

# TO DO
        
	- get rid of explicit declaration of static variables. let the key= do the creation ?	

    - Solve the view PDF documentaion problem. See the other todo doc.
 
    - Add a slider for the prevint ?
    
    -  Create documentation including a documentation vidio and deploy it
        - https://docs.python-guide.org/writing/documentation/

    - database ? any backend easy? what about that none backend one
      presumably a web url call.
       
     - security error
       Patched release and documentation
        See https://ipython.readthedocs.io/en/stable/whatsnew/version8.html#ipython-8-0-1-cve-2022-21699,
        
        Version 8.0.1, 7.31.1 for current Python version are recommended.
        Version 7.16.3 has also been published for Python 3.6 users,
        Version 5.11 (source only, 5.x branch on github) for older Python versions.
    
    - WARNING: You are using pip version 22.0.3; however, version 22.0.4 is available.
            To install a particular version (say earlier) pip install pip==1.2.1
            
    # For final submission.
    # - check results carefully.
    # - create an actual test case of a specific covid screening test.
"""

# IDE USED TO DEVELOP THIS CODE
# - Python: Version: 3.9.7
# - Ipython: Version: 7.29.0  :
       # security issue. Recommend upgrading ipython to version 7.31.1
       # https://github.com/ProfBrockway/ScreeningTest/security/dependabot/2
# - Anaconda: Version: 4.11.0
# - Spyder: # Name             Version        Build  Channel
#             pyls-spyder      0.4.0          pyhd3eb1b0_0
#             spyder           5.1.5          py39haa95532_1
# - O/S: Windows 10
# - pip: 21.2.4 from C:\Users\Brock\anaconda3\lib\site-packages\pip(python 3.9)
#
import sys

import os
import streamlit as st
from streamlit import session_state as S
import pandas as pd
import matplotlib as mpl  

# Plotly imports. Some may be flagged as unused, but import them anyway.
import scipy # Used by plotly figure factory behind the scenes.
import plotly
import plotly.express as px 
import plotly.figure_factory as ff
import plotly.graph_objects as go


class Global_Variables():  # A class creating all global variables.
    ###########################################################################    
    # +++ DETAILS ABOUT THIS MODULE
    ThisModule_Project = "Medical Screening Tests Efficacy."
    ThisModule_Version = "7_01   2022 March 9."  
    ThisModule_About = "For a course Spring 2022. "  
    ThisModule_Author = "TB, UConn Math Dept."
    ThisModule_Purpose = ("To demonstrate the effect of disease prevalence " 
                         "on the reliability of medical screening tests.")
    ThisModule_Contact = "Contacts not supplied."
    ThisModule_Docstring = (__doc__)
    ThisModule_FullPath  = os.path.abspath(__file__)
    ThisModule_FileName = os.path.basename(ThisModule_FullPath)
    ThisModule_ProjectPath = os.path.dirname(ThisModule_FullPath)
  
    
    # +++ RESOURCE LINKS Etc  Pictures/Videos/Files etc stored online.
    #   Where possible we base our resources in this apps repostitory
    #   at github. If github basing is not possible or inadequate
    #   we have to use another cloud storage site, eg Google drive.
         
    # Program Help/Documentation.    
    Link01 = ("https://github.com/ProfBrockway/ScreeningTest/" 
             "blob/main/Resource_App_Documentation_Full.pdf")
    # Project Folder at Github.
    Link02 = "https://github.com/ProfBrockway/ScreeningTest"
    # Where to report a bug.
    Link04 = "https://www.ibm.com/us-en?ar=1"  
    # App documentation video.
    Link20 = "https://youtu.be/DkpuAnnDjyo"
    # Name of downloaded table file
    Link40 = "ScreeningTestDataFrame.csv"
    
    Debug = False
    # +++ END OF RESOURCES AND OTHER LINKS OR VARIABLES THAT MIGHT CHANGE.
    ###########################################################################
 
    # ++++  THE STATITICAL VARIABLES OF THE MEDICAL SCREENING TEST  ++++++++++

    # ++ POPULATION SIZE: The number of people in the test data population.
    # PopulationSize = TP+FP+TN+FN  # Pop should add up to these 4 items.
    PopSize = None    # Population is input by the user.

    # ++ SENSITIVITY aka TPR aka (True Positive Rate).
    #  Sensitivity is the ability of a test to correctly identify people
    #  WITH the disease.
    #  Sensitivity is the proportion of test positives that are correct.
    #    'Correct' means the test is positive & person is infected).
    #  Sensitivity = TPR = (TP)/(TP + FN)
    #              =  Number Of True Positives
    #                           /
    #            (Total Number Of  Infected People In The Population)
    Sens = None      # Sensitivity is input by the user.

    # ++ SPECIFICITY aka TNR (True Negative Rate)
    #  Specificity is the ability of a test to correctly identify people
    #  WITHOUT the disease.
    #  Specificity is the proportion of test negatives that are correct.
    #    'Correct' means the test is negative & person is not infected).
    #  SPECIFICITY = TNR = (TN) / (TN + FP)
    #              =  Number Of True Negatives
    #                          /
    #          (Total Number Of Uninfected People In The Population)
    Spec = None      # Specificity is input by the user.

    # ++ TP  True Positive:
    # Ie: When the test result is positive & testee IS infected.
    # TP = PopulationSize * PopulationPrevalence * Sensitivity.
    TP = None

    # FP  False Positive:
    # A False Positive result.
    # Ie: When the test result is positive & testee is NOT infected.
    # FP = PopulationSize * (1 - PopulationPrevalence) * (1 - Specificity)
    FP = None

    # ++ TN  True Negative:
    # A True Negative result.
    # Ie: When the test result is negative & testee is NOT infected.
    # TN = PopulationSize * (1 - PopulationPrevalence) * Specificity
    TN = None

    # ++ FN  False Negative:
    # A false negative result.
    # Ie: When the test result is negative & testee IS infected.
    # FN = PopulationSize * PopulationPrevalence * (1 - Sensitivity)
    FN = None

    # ++ PPV: Positive Predictive Value
    # The PPV is probability that a subject IS infected given that he
    # or she tested positive for it.
    # Eg: A PPV = 11% means that of those who test positive only 11% are
    # really infected.
    # PPV = TP / (TP + FP)
    PPV = None
    
    # FPPercent  False Positive Percentage of all positives.
    # FPPercent = 1 - PPV
    FPPercent = None

    # ++ NPV: Negative Predictive Value
    # The NPV is the probability that a subject IS actually NOT infected
    # given that he or she tested negative for it.
    # Eg: A NPV = 11% means that of those who test negative only 11% are
    # really negative.
    # NPV = TN / (TN + FN)
    NPV = None

    # ++ ACC: Accuracy: = ((TP + TN)) / Pop
    # The "Overall Accuracy” is the specious measure sometimes used to (IMHO)
    # create a misleading impression that a screening test is usful when
    # in fact it is dangerously misleading.
    Acc = None

    PrevInt_FPPercent = 0
    PrevInt_FNPercent = 0
    
    # THE RANGE OF PREVALENCES
    # A list to contain all the Prevs we will test and graph.
    PrevList = list([])
    PrevStart = None       # PrevStart is input by the user.
    PrevEnd = None         # PrevEnd is input by the user.
    PrevInt = None         # PrevInt is input by the user.

    # THE DATATABLE
    # The DataTable is a pandas dataframe (data table) to store our results.
    # - This program tests a range of values for prevalences [0 , 1]
    # - Each table row stores the results for a particular 'prevalence'.
    DataTable = pd.DataFrame(
        columns=["Prevalence",
                 "TP",
                 "FP",
                 "TN",
                 "FN",
                 "ACC",
                 "Sens",
                 "Spec",
                 "PPV",
                 "FPPercent",
                 "NPV",
                 "PrevInt",
                 "FNPercent",
                 "Population" 
                ]
                               )

    # SUNDRY GLOBAL VARIABLES
    Fig1 = None
    Plot1 = None
    Fig2 = None
    Plot2 = None
    Msg01 =  "Enter the parameters of the medical screening test "\
             "and click 'Plot Now' button."
    Plot_Report_Short = None
    Plot_Report_Long = None
    False_Pos_Message = None
    False_Neg_Message = None    

 
    
# End of Global Variables
G = Global_Variables()    # Instantiate our global variables.

def MainLine():
    # Remember this app is run every time the GUI is displayed and 
    # the "form run button" is clicked by the user.
    # So we have to keep track of the conversation state.
        
    ConsoleClear()  # Clear the internal IPyhon console.

    # If this the initial session create "Static/Persistent" variables.
    if 'Dialog_State' not in S:
        Initialization_Perform_First_Load_Only()
        S.Dialog_State  = 1  # Upgrade state so we don't come back here.

    else:  # We are responding to a session reply from the user.
        S.Display_Count += 1  # Count of sessions.
        
        # Initalize variables for every run.
        #   Remember nothing outside the Streamlit Static/persistant dictionary
        #   is preserved across sessions. So we perform the one time
        #   program initialization once then perform the "every run"
        #   Initialization.
        Initialization_Perform_EveryRun()
        
        # Validate and internalize users'input.
        InputOK = User_Input_Validate_And_Internalize()
        if InputOK == True:
            # Build a table for the efficacies of the screening test across
            # the range of disease prevalences specified by the user.
            User_Input_Process()
            # Plot the table of efficacies of the screening test.
            GUI_Right_Panel_Build()
            
        else:  # There is an error in the users input. 
           st.error(G.Msg_Current) # Show the error in the right panel.

    # Display the results and wait for next user input.
    GUI_Build_Basic_Layout()
    return()  # End of function: MainLine.

def Initialization_Perform_EveryRun():
    # Initalize variables for every run.
    #   Remember nothing is preserved across sessions, except variables in  
    #   the streamlit static "session_state" dictionary.
    #  
    #   On the first run we perform the one time program initialization.
    #   On subsequent runs we perform the "every run" Initialization to 
    #   initialize or reinitialize anything not preserved across 
    #   the display/response dialog.
    # 
    # Alternatives to repeating initialization here are: 
    # (1) Save static/persistant variables in the streamlit "session_state".
    # (2) Make the initialization "static" using streamlit st.cache.
    #      - Use st.cache if the initialization is very time consuming.
    # (3) Initialize in our Global_Variables class (above)
    #     The Global_Variables class is run everytime the app is run.
    #     So it initializes every time streamlit reruns this app.
    #
    # However having an "Every Time" initialization function is good practice.
    # It may be neccessary to make the logic work.
    # Also its less vulnerable to the subtle misbehaviors of alternatives
    # (1) and (2).
 

    
 
    return()

def Initialization_Perform_First_Load_Only():

    # Initalize variables etc.
    Initialization_Perform_EveryRun()

    # This must be the FIRST streamlit function in the program.
    # This must be called only once.
    GUI_HelpMenu_Build()
       
    # Static variables are static, persistant and global.  
    Static_Variables_Create() 
       
    return()  # End of function: Initialization_Perform_First_Load_Only

def User_Input_Validate_And_Internalize():
    # - This function validates the users input.
    # - This function also internalizes the users input.
    #     -Internalization isolates the data processing from the GUI.
    #     -Internalization is achieved by transfering the input values
    #      from the streamlit persistant session_state dictionary to 
    #      regular python variables in our global variable class.
    #    - We are using streamlit for our GUI but that may be replaced.
    #      Also streamlit has some nasty bugs we don't want complicating
    #      the data processing code.
    #
    # - The Streamlit input widgets perform validation for data type 
    #   and values ranges.
    #      - Eg: A widget can be set up to disallow a number input 
    #        that is not numeric.
    #      - So most of the following validations are duplicative.
    #        But I have left them in as belt and suspenders.
    
    S.MsgText = ""   

    G.PopSize, InputOK = Validate_Integer(S.PopSize)
    if InputOK == False:
       Msg_Set("Error 1006: Population size must be an integer.") 
       return(False) 
    if G.PopSize < 100:
       Msg_Set("Error 1008: Population size must at least 100.")  
       return (False)
    
    G.Sens,InputOK = Validate_Float(S.Sens)
    if InputOK == False:
       Msg_Set("Error 1010: Sensitivity must be numeric.")
       return (False)
    if (G.Sens < 0) or (G.Sens > 1):
       Msg_Set("Error 1012: Sensitivity Invalid. Must be [0,1] ")
       return (False)
   
    G.Spec, InputOK = Validate_Float(S.Spec)
    if InputOK == False:
       Msg_Set("Error 1014: Specificity must be numeric.")
       return(False)
    if (G.Spec < 0) or (G.Spec > 1):
       Msg_Set("Error 1016: Specificity Invalid. Must be [0,1] ")
       return(False)
   
    G.PrevStart, InputOK = Validate_Float(S.PrevStart)
    if InputOK == False:
       Msg_Set("Error 1018: Prevalence Start must be numeric.")
       return(False)
    if (G.PrevStart < 0) or (G.PrevStart > 1):
       Msg_Set("Error 1020: Prevalence Start Invalid. Must be [0,1] ")
       return(False)
   
    G.PrevEnd, InputOK = Validate_Float(S.PrevEnd)
    if InputOK == False:
       Msg_Set("Error 1018: Prevalence End must be numeric.")
       return(False)
    if (G.PrevEnd < 0) or (G.PrevEnd > 1):
       Msg_Set("Error 1020: Prevalence End Invalid. Must be [0,1] ")
       return(False)

    G.PrevInt, InputOK = Validate_Float(S.PrevInt)
    if InputOK == False:
       Msg_Set("Error 1022: Prevalence of Interest must be numeric.")
       return(False)
    if (G.PrevInt < 0) or (G.PrevInt > 1):
        Msg_Set("Error 1026: Prevalence Of Interest Must be [0,1]")
        return(False)
    if (G.PrevInt < G.PrevStart) or (G.PrevInt > G.PrevEnd):
       Msg_Set("Error 1030: Prevalence Of Interest "\
                "must lie between Prevalence Start and Prevalence End.")
       return(False)
 
    # If we fall through here the users input is all valid.
    S.MsgText = G.Msg01    # Reset the "Please enter test specs" message.
    return(True)  # End of function: User_Input_Validate_And_Internalize

def User_Input_Process():
    # Build table of statistics for the specified range of prevalences.
    # For the specified range of prevalences (Eg Prevs from 0% to 100%) build
    # a table with a row for each prevalence in the range and that
    # prevalences' statistics.

    # Create a list of population disease prevalences percentages
    # over which  we  want to test the efficacy of the screening test.
    G.PrevList.clear()   #  Instantiate the list of prevalences.
    
    # Avoid zero divide by altering a zero prevalence to a near zero number.
    if G.PrevStart == 0:
        G.PrevStart = 0.00000000000000000001
        
    # The increment controls the number of data points on the x axis.    
    prev_increment = (G.PrevEnd - G.PrevStart) / 100
    i = 0
    G.PrevList.append(G.PrevStart)
    while G.PrevList[i] < G.PrevEnd:
        G.PrevList.append(G.PrevList[i] + prev_increment )
        i = i + 1

    # Process each of the Prev's in the list of Prev's to be tested.
    # The stats for each prev are calculated and stored in a table row.
    G.DataTable = G.DataTable[0:0] # Clear the DataTable. Retain its structure.
    
    # We will make a note of the false positive and negative rates at the
    # users prevalence of interest.
    G.False_Pos_Message = "" 
    G.False_Neg_Message = "" 
    
    # Add rows to the DataTable
    for PrevCurrent in G.PrevList:  
        # TP  True Positive:  The test is positive & testee is infected.
        # TP = PopulationSize * PopulationPrevalence * Sens.
        G.TP = G.PopSize * PrevCurrent * G.Sens
    
        # FP  False Positive:  Test is positive & testee is NOT infected.
        # FP = PopulationSize * (1 - PopulationPrevalence) * (1 - Spec)
        G.FP =   G.PopSize * (1 - PrevCurrent) * (1 - G.Spec)
    
        # TN  True Negative: Test is negative & testee is NOT infected.
        # TN = PopulationSize * (1- PopulationPrevalence) * Spec
        G.TN = G.PopSize * (1 - PrevCurrent) * G.Spec
    
        # FN  False Negative: The test is negative & testee IS infected.
        # FN = PopulationSize * PopulationPrevalence * (1 - Sens)
        G.FN = G.PopSize * PrevCurrent * (1 - G.Sens)
    
        # Sens: Sens aka TPR / (True Positive Rate)
        # The proportion of test positives that are correct.
        # (When the test is positive & person IS infected).
        G.Sens = G.TP / (G.TP + G.FN)
    
        # Spec: Spec aka TNR (True Negative Rate)
        # The proportion of test negatives that are correct.
        # (When the test is negative & person is not infected).
        G.Spec = G.TN / (G.TN + G.FP)
    
        # PPV: Positive Predictive Value
        # The probability that a testee is infected given & tested positive.
        # Eg: A PPV = 11% means that of those who test positive only
        #     11% are infected.
        G.PPV = G.TP / (G.TP + G.FP)
        
        # FPPercent. The percentage of all positives that are false.
        G.FPPercent =  1 - G.PPV
                
        # NPV: Negative Predictive Value
        #  The probability that a testee is infected & tested negative.
        G.NPV = G.TN / (G.TN + G.FN)
        
        # FPPercent. The percentage of all negatives that are false.
        G.FNPercent =  1 - G.NPV
            
        # ACC: Accuracy: = ((TP + TN)) / Pop
        G.Acc = (G.TP + G.TN) / G.PopSize
        
        # Add the stats for the Population Prevalence we have just processed
        # to our results table, DataTable if required.
        newrow = {'Prevalence' : PrevCurrent,
                  'TP'         : G.TP,
                  'FP'         : G.FP,
                  'TN'         : G.TN,
                  'FN'         : G.FN,
                  'ACC'        : G.Acc,
                  'Sens'       : G.Sens,
                  'Spec'       : G.Spec,
                  'PPV'        : G.PPV,
                  'FPPercent'  : G.FPPercent,
                  'NPV'        : G.NPV,
                  'FNPercent'  : G.FNPercent,
                  'PrevInt'    : G.PrevInt,
                  'Population' : G.PopSize
                  }
        
        # Find the percentage of positives that is false.
        if (PrevCurrent >= G.PrevInt) and (G.False_Pos_Message == "" ):
            # Stop search. We are near the prevalence of interest.
            G.PrevInt_FPPercent = G.FPPercent # Save the FP percentage.
            G.False_Pos_Message = (
                "About " + 
                str( "{:.2f}".format(G.FPPercent * 1)) + 
                " of all positives are false at a prevalence of " +
                "{:.6f}".format(G.PrevInt) + 
                "."                )            
                         
         # Find the percentage of negatives that is false.
        if (PrevCurrent >= G.PrevInt) and (G.False_Neg_Message == "" ):
            # Stop search. We are near the prevalence of interest.
            G.PrevInt_FNPercent = G.FNPercent  # Save the FN percentage.
            G.False_Neg_Message =(
                "About " + 
                str( "{:.2f}".format(G.FNPercent * 1)) + 
                " of all negatives are false at a prevalence of " +
                "{:.6f}".format(G.PrevInt) + 
                "."                )     
        
        G.DataTable = G.DataTable.append(newrow, ignore_index=True)
    
    # End of 'For each PrevCurrent'

    return # End of function: User_Input_Process

def GUI_Build_Basic_Layout():        # Build the GUI.
    # - Our GUI is a streamlit web page with widgets in a vertical toolbar 
    #   on the left and a plot and display area on the right.
    #
    #   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # - !!!!! DON"T ADD A "value=" parameter to any input widget. !!!!!!
    #      The "val=" causes error messages about duplicate initialization.
    #       Instead let the static variable created by the key= parameter
    #       do the work.
    #
    #  - Widget values are stored in "linked" streamlit persistent variables.
    #     The value input/output to/from each widget is stored in/retrieved 
    #     from a streamlit "linked" persistant variable linked to the 
    #     widget's by the widgets "key=" parameter. See elsewhere in this
    #     program for an explanation of "linked" static variables.
    
    # - We now make the sidebar a single form with a single submit button.
    #    With st.form and its form_submit_button, this app only reruns
    #    when you hit the form submit button, NOT at each widget interaction.
    #    https://blog.streamlit.io/introducing-submit-button-and-forms/
    Form1 = st.sidebar.form(key="Form1", clear_on_submit=False)

    with Form1:

        # Create a textbox for displaying instructions and error messages.
        st.text_area(
            key="MsgText",   # Value will be placed in S.MsgText'].
            label="INSTRUCTIONS",
            height=None,
            max_chars=None,
            help="This box offers instructions and reports errors in input.",
            on_change=None)

        # Add a form submit button.
        # Every "form" must have exactly one form_submit_button.
        st.form_submit_button(
                    label='Plot Now',
                    on_click=PlotNowButton_Click_Event,
                    help="When you have entered the parameters  \r"
                    "for the calculations click this  \r"
                    "button to draw your plot.",
                    args=(),
                    kwargs=())

        # Create input boxes in the toolbar for our user specifed variables.
        # Input the Population Size.
        st.number_input(
            key="PopSize",        # Value will be placed in S.MsgText'].
            label="Population",
            min_value=1,
            max_value=1000,
            step=None,
            format="%i",
            help="Enter the population.[100,1000]. "
                 "Population does not effect  "
                 "the results which are all percentages of population. "
                 "Changing Population changes the number of data points. ",
            on_change=None,
            args=None,
            kwargs=None,
            disabled=False)

        # Input the Test Sensitivity.
        st.number_input(
            key="Sens",              # Value will be placed in S.Sens'].
            label="Sensitivity",
            min_value=0.00,
            max_value=1.0,
            step=0.01,
            format="%f",

            help="Enter the tests' Sensitivity. [ 0, 1]",
            on_change=None)

        # Input The Test Specificity.
        st.number_input(
            key="Spec",          # Value will be placed in S.Spec'].
            label="Specificity",
            min_value=0.00,
            max_value=1.0,
            step=0.01,
            format="%f",
            help="Enter the tests' Specificity. [ 0, 1 ]",
            on_change=None)

        # Input the start of the range of prevalences to be tested.
        st.number_input(
            key="PrevStart",  # Value will be placed in S.PrevStart'].
            label="Prevalence Start",
            min_value=0.00,
            max_value=0.99,
            step=0.01,
            format="%f",
            help="Enter the start of the range of prevalence "
                "to be plotted. [ 0, 0.99 ]",
            on_change=None)

        # Input the end of the range of prevalences to be tested.
        st.number_input(
            key="PrevEnd",  # Value will be placed in S.PrevEnd'].
            label="Prevalence End",
            min_value=0.00,
            max_value=1.00,
            step=0.01,
            format="%f",
            help="Enter the end of the range of prevalences to be plotted."
                  " [ 0.01, 1 ]",
            on_change=None)

        # Input the prevalence of interest to be highlighted on the plot
        st.number_input(
            key="PrevInt",    # Value will be placed in S.PrevInt'].
            label="Prevalence Of Interest",
            min_value=0.00,
            max_value=1.00,
            step=0.01,
            format="%f",
            help="Enter the prevalence of number_input. "
                  "A vertucal line will highlight"
                  " the values at the requested prevalence. [ 0.0,  1 ]",
            on_change=None)
 
        # Add checkboxes for selecting the lines to be shown on plot.
        



    return()  # End of function: GUI_Build_Basic_Layout

def GUI_Right_Panel_Build():  # Put the plot etc in the GUI right panel.
    
    ###########################################################################
    # +++ BUILD THE PLOT REQUESTED BY THE USER AND PLACE IT ON THE GUI.
    # Increase the visibility of the Streamlit "full page" icon.
    Plot_Streamlit_FullScreenIcon_Format()
     
    # Build the plot using Plotly graph objects (GO)(not plotly express).
    Plot_Build_Plotly_GO()    
    
    st.info("🟢 HERE IS THE PLOT YOUR REQUESTED")
    
    # Display a Plot Report box on the GUI.
    st.text(Plot_Report_Build(formatfor="regular")) 
        
    # Place the Plotly plot on the GUI.
    #  use_container_width
    #      If True, set the chart width to the column width. 
    #     This takes precedence over the figure's native width value.
    #     Don't set height or width anywhere. Let Streamlit and Plotly
    #     scale everything. Otherwise the GUI won't adjust properly to
    #     different size screens.
    st.plotly_chart(G.Fig1, 
                    use_container_width=True, 
                    config={'displayModeBar': True}, # Force plotly toolbar.
                    sharing="streamlit")
    
    # Build the plot using Plotly Express (not plotly G) [Graph Objects]).
    Plot_Build_Plotly_EX()    
    st.plotly_chart(G.Fig2, 
                    use_container_width=True, 
                    config={'displayModeBar': True}, # Force plotly toolbar.
                    sharing="streamlit")
    
    ###########################################################################
    # +++ MAKE THIS APPS DOCUMENTATION AVAILABLE.
    #   We  base the pdf file in the github repository for the project.
    #   The github using the github link to the address displays
    #   the pdf file in the primitive github pdf view which does not
    #   have basic features, especially the pdf document index.
    #   I have not been able to fix this problem so for now, the pdf
    #   is displayed and the user advised to download it a use a 
    #   proper pdf viewer.
    st.info("🟢 THIS APP'S DOCUMENTATION.")
       
    col1, col2 = st.columns(2)
    with col1:
        st.write(" [ Link To This App's Documentation.]"  "(%s)" % G.Link01)
        st.write(" [ Link To All Of The Projects Files.]"  "(%s)" % G.Link02)
    with col2: 
        # Display a pop up help message to help accessing documentation.
        # We use an st.button and load its help parameter with our popup.
        # This works fine when the user hovers the mouse over the button.   
        # But when the user clicks the button (as is reasonable) the
        # app is rerun. This doesn't produce any errors but is obviously
        # inefficient. We have to live with this until we find a better
        # method for pop up messages.
        tempstr = (""" You can read this app's documentation in the project's
        Gihub project 'repository'.   
        Click the links.           
        Github only provides primitive document viewers.
        So you may wish to download the files and view them on your computer.
        Then you will be able to navigate the documents using indexes, 
        navigation panes, search  etc.   
        You can also see the program documentation by using
        the menu in the top right of this webpage '≡' (3 horizontal lines) then
        select 'GET HELP'. """) 
        st.button(label="Help", key="ButtonH1", help=tempstr )

    
    ###########################################################################
    # +++ SHOW THE DATATABLE.
    st.info("🟢 THE DATA TABLE GENERATED BY YOUR PARAMETERS FOLLOWS")
    st.dataframe(data=G.DataTable, width=None, height=None)

    #  +++ ADD A "DOWNLOAD" DATAFRAME BUTTON.
    # - The dataframe is converted to a csv file.
    # - That file is downloaded to the browsers download location.
    # - There is no "save as" menu. The file name is hard coded.
    DataFrame_CSV = G.DataTable.to_csv().encode('utf-8')
    helpstr = f"""You can save the data frame to your computer using this button.  \r
        The file will be called {G.Link40}.   \r
        The file will be in CSV format, (Comma Separated Variable).   \r
        The file will be saved in your browser's default download location on your computer.  \r
        You can enlarge the table by clicking the 'View fullscreen' icon located at the top right of the table.  \r
        'Float' the mouse over the table and the 'View fullScreen' icon will appear.
         """
    st.download_button(label="⚙️ Download The DataFrame", 
                       data=DataFrame_CSV, 
                       file_name=G.Link40, 
                       mime= "text/csv",
                       key="DownloadCSV_Button", 
                       help=helpstr, 
                       on_click=None, 
                       args=None,
                       kwargs=None, 
                       disabled=False)

    ###########################################################################
    # +++ SHOW A VIDEO DEMONSTRATING THIS APP.
    #  Github basing of videos does not allow raw address of large files.
    #  Google basing of videos  does not work because it downloads too slowly.
    #  So until I can figure out how to base videos at github we use Youtube.
    st.info("🟢  A VIDEO DEMONSTRATING THIS APP'S FEATURES.")   
    st.video(G.Link20)
   
    return  # End of function: GUI_Right_Panel_Build

def GUI_HelpMenu_Build():
    # ++++ Set up a typical "About/Help" menu for the webpage.
    #  - The set_page_config command can only be used once per run.
    #  - The set_page_config command be the first Streamlit command used.
    #  - New line marker \n must be preceeded by at least two blanks to work.
    st.set_page_config  (
     page_title = "Webage Header. ", 
     
     page_icon = ":confused:",
     
     layout="centered", # or "wide".
        # 'wide' gives a bigger display. 
        # 'centered' gives a smaller display
        #  Remember that plots and tables etc on the streamlit webpage 
        #  can be "blownup" by the user clicking an "expand" icon.
        #  So don't worry if the normal view is too small.
     
     initial_sidebar_state="auto",
     
     # \r requires two preceeding spaces to work.
     menu_items={ # These appear as the webpage "about" menu items.
     'Get Help  ':  G.Link01,
     'Report a bug  ': G.Link04,
     'About': '  \rProgram: ' +  G.ThisModule_FileName 
            + '  \rProject:  ' + G.ThisModule_Project
            + '  \rProgram Purpose:  ' + G.ThisModule_Purpose 
            + '  \rAuthor:  ' +  G.ThisModule_Author   
            + '  \rContacts:  ' +  G.ThisModule_Contact
            +  '  \rVersion:  ' + G.ThisModule_Version               
               }
                      )
    return()  # End of function: GUI_HelpMenu_Build

def Plot_Build_Plotly_GO(): # Create our plot using Plotly Graph Objects.
    # Plotly graph objects (GO) are for building plots "by hand".
    # GO graphing gives more control than graphing with Plotly Express.
    
    # Create a graph of Prevalence (x axis) vs various statistics.
    # We build a line plot with multiple graph lines.
    # The user can also hide or show drawn lines  by clicking the plot's 
    # legend after the plot has been displayed.
             
    G.Fig1 = go.Figure() # Create an empty Plotly figure.
    
    # Plot all graph lines on one axis.
    # We add the lines(aka traces) to the plot that the user has requested.
     
    G.Fig1.add_trace(go.Scatter(
        name="False Positive Percentage", # Shows in Legend.
        text="False Positive Percentage", # Shows in Hovertext.
        legendrank=1, # Where the line will appear in the legend list.
        x=G.DataTable["Prevalence"], y=G.DataTable["FPPercent"], 
        visible=True,
        mode="lines",
        line=dict(color="red")  )) 
   
    G.Fig1.add_trace(go.Scatter(
        name="False Negative Percentage",
        text="False Negative Percentage",
        legendrank=2,
        x=G.DataTable["Prevalence"], y=G.DataTable["FNPercent"],
        visible="legendonly",
        mode="lines",
        line=dict(color="blue")  ))     

    G.Fig1.add_trace(go.Scatter(
        name="Positive Predictive Value",   
        text="Positive Predictive Value",   
        legendrank=3,
        x=G.DataTable["Prevalence"], y=G.DataTable["PPV"], 
        visible="legendonly",
        mode="lines",
        line=dict(color="green"  )   ))
  
    G.Fig1.add_trace(go.Scatter(
        name="Negative Predictive Values",
        text="Negative Predictive Values",
        legendrank=4,
        x=G.DataTable["Prevalence"], y=G.DataTable["NPV"], 
        visible="legendonly",
        mode="lines",
        line=dict(color="magenta")  ))
     
    G.Fig1.add_trace(go.Scatter(
        name="False Positive",
        text="False Positive",
        legendrank=6,
        x=G.DataTable["Prevalence"], y=G.DataTable["FP"], 
        visible="legendonly",
        mode="lines",
        line=dict(color="black")  ))

    G.Fig1.add_trace(go.Scatter(
        name="False Negative",
        text="False Negative",
        legendrank=8,
        x=G.DataTable["Prevalence"], y=G.DataTable["FN"], 
        visible="legendonly",
        line=dict(color="peru" ) ))
    
    G.Fig1.add_trace(go.Scatter(
        name="General Accuracy",
        text="General Accuracy",
        legendrank=9,
        x=G.DataTable["Prevalence"], y=G.DataTable["ACC"],
        visible="legendonly",
        mode="lines",
        line=dict(color="orange")  ))
    

    # We don't really need a vertical line at the prevalence of interest
    # because the plotly hover text does a better and dynamic job
    # of highlighting values of any statistic at any prevalence. 
    # Add a vertical line at the prevalence of interest.
    # G.Fig1.add_vline(x=G.PrevInt,line_dash="dash", line_color="red") 
    
    # Adjust titles, grid, font etc.
    G.Fig1.update_layout(title="<b>Screening Test Statistics",title_x=0.4)
    G.Fig1.update_layout(xaxis_title="<b>Disease Prevalence In Population")
    G.Fig1.update_layout(yaxis_title="<b>Response Of The Screening Test")
    G.Fig1.update_xaxes(showgrid=True,gridcolor="lightgray")
    G.Fig1.update_yaxes(showgrid=True,gridcolor="lightgray")
    # We let the plot autosize so that it will best fit different
    # size screens. 
    G.Fig1.update_layout(autosize=True, width=None, height=None) #800*1100
    G.Fig1.layout.plot_bgcolor = "white"
    G.Fig1.layout.margin = dict(t=5, b=5, l=0, r=0)
        
    # Adjust the hover text aka "mouseover" text.
    # Show hover values for all visible lines (aka traces).
    G.Fig1.update_layout(hovermode="x") # Also "x unified" or "closest"
    # Show vertical and horizontal hover axes intersect lines.
    G.Fig1.update_xaxes(showspikes=True)
    G.Fig1.update_yaxes(showspikes=True)
    # Specify what is shown on each hovertext line.
    G.Fig1.update_traces(
    hovertemplate="<br>".join(["at Prevalence: %{x:.4f}","Value: %{y:.4f}"]))
    # Alter the hovertext font.  
    G.Fig1.update_layout(hoverlabel=dict(font_size=12,bgcolor="palegreen")) 
  
    # Adjust the legend.
    G.Fig1.update_layout(legend_title_text="<b>Legend.")
    G.Fig1.update_layout(
    legend=dict(
        # title_font_family="Times New Roman",
        font=dict(size=10),
        # Make the legend transparent to minimize its obscuration of the plot.
        bgcolor="rgba(0,0,0,0)", 
        bordercolor="Black",
        borderwidth=1 ))
    # Place the legend at a desired location on the plot.
    # The legend will sometimes obscure the plot.
    # So we place it to the right of the plot.
    # This reduces and reshapes the plot display itself.
    # Fortunately the Plotly "full screen" option can be used to view the plot
    # beautifully.
    G.Fig1.update_layout(
      legend={"yanchor":"middle","y":+ 0.50,"xanchor":"right","x":+1.35})
    
    
    # Adjust the axes tick marks.
       # Since the range of prevalences on the xaxis varies we have
       # to vary the tick frequency on the xaxis. 
    XtickIncrement = (G.PrevEnd - G.PrevStart) / 10
    G.Fig1.update_layout(xaxis = dict(tickmode = 'linear',
                         tick0 = G.PrevStart, dtick = XtickIncrement))
    G.Fig1.update_layout( yaxis = dict(tickmode = 'linear',
                          tick0 = 0, dtick = 0.1))
        
    # Add border around the plot. #,ivory,linen,mintcream,snow,whitesmoke
    G.Fig1.update_layout(
        margin=dict(l=10, r=10, t=30, b=30), paper_bgcolor="mintcream", ) 
    G.Fig1.update_xaxes(showline=True,  linecolor='black', mirror=True)
    G.Fig1.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    
    # Add a documentation text box to the plot.
    #  This works if you make the plot area big enough to put the
    #  document box under the plot. (See width/height above.)
    #  But if we don't autosize the plot it won't adjust to different size
    #  screens. So we avoid any feature that sets absolute size for anything.
    
    # G.Fig1.add_annotation(
    #     text=Plot_Report_Build(formatfor="streamlit"), 
    #         align="left",
    #         showarrow=False,
    #         xref="paper", yref="paper",
    #         x= 0.40, xanchor = "left",
    #         y=-0.25, yanchor = "bottom",
    #         bordercolor="black", borderwidth=0)
        
    return() # End of function:   Plot_Build_Plotly_GO()

def Plot_Build_Plotly_EX():  #?V
   
    G.Fig2 = px.line(G.DataTable, 
       x="Prevalence", 
       y=[
           "FPPercent",
          "FNPercent",
          "PPV",
          "NPV",
          "FP",
          "FN",
          "ACC",
         ],
       color_discrete_map={
          "FPPercent": "red",
          "FNPercent": "blue",
          "PPV": "green",
          "NPV": "magenta",
          "FP": "black",
          "FN": "peru",
          "ACC": "orange"
                      },
       labels={
          "FPPercent": "False Positive Percent",
          "FNPercent": "False Negative Percent",
          "PPV": "green",
          "NPV": "magenta",
          "FP": "black",
          "FN": "peru",
          "ACC": "orange"
          },

       template="simple_white"
       )
    
    NewLabels={
          "FPPercent": "False Positive Percent",
          "FNPercent": "False Negative Percent",
          "PPV": "Positive Predictive Value",
          "NPV": "Negative Predictive Vallue",
          "FP": "False Positive",
          "FN": "False Negative",
          "ACC": "Overall Accuracy"
          },

    
    
    
    return()  # End of function: Plot_Build_Plotly_EX().


def Plot_Report_Build(TitleLength = "long",formatfor="regular"):
    G.Plot_Report_Short = str(
                   "\n\nScreening Test Statistics \n" +
                   "As The Disease Population Prevalence Varies From " +
                   "{:.5f}".format(G.PrevStart)  +
                   " To {:.5f}".format(G.PrevEnd) + "."
                           )
   
    G.Plot_Report_Long =  G.Plot_Report_Short + "  \n" + str(
      "Population = {:,}   \n".format(G.PopSize) +
      "Sensitivity = {:.4f}   \n".format(G.Sens) +
      "Specificity = {:.4f}   \n".format(G.Spec) +
      "Prevalence Start = {:.5f}   \n".format(G.PrevStart) +
      "Prevalence End = {:.5f}   \n".format(G.PrevEnd) +
      "Prevalence Of Interest = {:.6f}   \n".format(G.PrevInt) +
      G.False_Pos_Message + "  \n" +
      G.False_Neg_Message
                                                ) 
    
    # If the text is intended for an html text target use the html line break.
    if formatfor == "streamlit":
        G.Plot_Report_Long = G.Plot_Report_Long.replace("\n", "<br>")
    if TitleLength == "short":
        G.Plot_Report_Long = G.Plot_Report_Short
    
    return(G.Plot_Report_Long)   #  End of function: Plot_Report_Build

def Plot_Streamlit_FullScreenIcon_Format():
    # This function increases the visibility of the Streamlit
    # full page icon..
    style_fullscreen_button_css = """
         button[title="View fullscreen"] 
         {background-color: #004170cc; left: 2; color: white; }
    
         button[title="View fullscreen"]:hover 
         {background-color: #004170; color: white; } """
    
    st.markdown( "<style>" 
                + style_fullscreen_button_css
                + "</styles>",
                unsafe_allow_html=True,
               )

def PlotNowButton_Click_Event():
    # Not used.
    # This function is Included to demonstrate that streamlit widgets have a
    # typical "callback" event option.
    return()  # End of function: PlotNowButton_Click_Event

def ConsoleClear():  # Clear all output in console.
    try:     # This works regardless of Operating System prevailing.
        from IPython import get_ipython
        get_ipython().magic("clear")
        get_ipython().magic("reset -f")
    except:
        pass
    return()  # End of function: Console_Clear

def Validate_Float(TextString):
    try:
        tempvar = float(TextString)
    except:
        return (0,False)
    else:
        return(tempvar,True)

def Validate_Integer(TextString):
    try:
        tempvar = int(TextString)
    except:
        return (0,False)
    else:
        return(tempvar,True)

def Msg_Set(TextString):
    FormattedText = TextString
    ErrStr = TextString[0:5].upper()  
    if ErrStr == "ERROR":
       FormattedText = (f"❌  There is an error in your input {FormattedText}"
                        "\nPlease correct and try again.")
    S.MsgText = FormattedText
    G.Msg_Current = FormattedText
    return()

def StMarkdown(TextToBeFormated="", color="black",
    fontsize=14,bold=False,italic=False,fontname="Courier",align="left" ):
    # Set a particular font for display as html markdown text.
    weight = ""    
    weightend = ""
    if bold:
        weight = "<strong>"    
        weightend = "</strong>" 
    if italic:
        weight = "<em>"    
        weightend = "</em>"  
    if bold and italic:
        weight = "<em><strong>"    
        weightend = "</em></strong>"
        
    fs = str(fontsize).strip() + "px"
    md = " ".join(
                  ["<p",
                      "style='",
                              "font-family:", fontname, ";",
                              "color:", color, ";",
                              "font-size: ",  fs, ";",
                              "text-align: ",  align, ";",
                           "'"
                  ">",
                        weight + TextToBeFormated + weightend ,
                  "</p>"]
               )
    return(md)  # End of function: StMarkdown

def Static_Variables_Create():         
    # +++ CREATE PERSISTENT/STATIC VARIABLES.
    # https://docs.streamlit.io/library/api-reference/session-state
    # During the first load session, we create our "Persistent" variables.
    #  Persistent variables:
    #   - Are stored and created by streamlit in the streamlit
    #     'session state dictionary'
    #   - Are static (preserved) between sessions.
    #   - Are effectively global.
    #   - Have a python dictionary like syntax.
    #   - Are created using the streamlit "session_state" method.
    #       - Eg:  st.session_state['Display_Count'] = 0
    #       - In our case the st.session_State is abbreviated to Static.
    #          - from streamlit import session_state as Static
    #          - Eg: S.Input_SSN'] = 0
    #   - Can be "linked" to a streamlit widget via the widget key= parameter.
    #      - Using the key= parameter on any widget automatically
    #        creates a static variable in the 'session state dictionary'.
    #        But I prefer to declare them explicity as well.
    #      - Any change in the Static linked widget will automatically update 
    #      - the linked persistant variable.
    #      - Any change in linked persistant variable will automatically 
    #        update the linked widgets value in th Static.
    #      - The python type of linked variables are specifed by the
    #        linked widget's  "format=" parameter.
    #
    #      - Eg of a Linked persistent variable.
    #         In this initialization section:
    #              S.FirstName'] = "Fred" # Create a persistant variable.
    #         In the Static creation code:
    #             st.number_input(label=:Enter first name", key="FirstName")
    #         Notice the key is the same as the persistent variable name.

    S.Dialog_State = 0    # Create session Dialog_State variable.
    S.Display_Count = 1   # A Count of sessions.

    # Persistant variables for the users input in the GUI
       
    S.MsgText = G.Msg01     # A text box for instructions & errors.
    S.PopSize = 100         # Test population.
    S.Sens = 0.99           # Test sensitivity.
    S.Spec = 0.99           # Test specifcity.
    S.PrevStart = 0.0       # Start of range of prevalences to plot.
    S.PrevEnd = 1.0         # End of range of prevalences to plot.
    S.PrevInt = 0.03        # Prevalence to be highlighted on plot.
    
    return() # End of function: Static_Variables_Create


MainLine()   # Start this program.


