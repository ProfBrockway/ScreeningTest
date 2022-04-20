
#TO DO
# search ?V
#  - We report (e.g.) the claimed absolute numbers of true positives. Add an 'adjusted' for prevalence actual true positives to the report.
#  - Create documentation including a documentation video and deploy it
# 
# For final submission.
# - Do hand calculations for verification.
#  - spell check comments to get rid of gross errors.
# - check results carefully against another calculator.


##############################################################################
#                           ScreeningTest
##############################################################################
# Course: CCSU Stat 476.  Spring 2022.
# Author: Tim Brockway. Student ID: 30259316   Email: BrockwayTim@My.CCSU.edu
# Professor: Roger L. Bilisoly
#     bilisolyr@ccsu.edu  https://www2.ccsu.edu/faculty/bilisolyr
# Program: screeningtest.py
# Purpose: To demonstrate the effect of disease prevalence on the
#          reliability of medical screening tests.
###############################################################################

############################################################################### 	 
#                      How To Run This Program.
#
# - Enter the following link into a web browser.
# - The web page will then explain how to run the program and its plots.
# https://share.streamlit.io/profbrockway/screeningtest/main/screeningtest.py
#
###############################################################################

###############################################################################
#           How To Run This Program On A Development Computer. 
#  - To test the app on a local (undeployed) server and see our web page
#    locally, enter the following command in the Anaconda console.
#  streamlit run "G:\My Drive\UConn\1-Subjects\Python\STAT476\CODE\ScreeningTest\screeningtest.py"
###############################################################################

import os
import streamlit as st
from streamlit import session_state as S
import pandas as pd

# Sundry imports. Some may be flagged as unused, but import them anyway.
import matplotlib as mpl    # We may use both matplotlib and plotly
import plotly
import plotly.express as px 
import plotly.graph_objects as go

from io import BytesIO
from pyxlsb import open_workbook as open_xlsb

class Global_Variables():  # A class creating all global variables.
    ###########################################################################    
    # +++ DETAILS ABOUT THIS MODULE
    ThisModule_Project = "Medical Screening Tests Efficacy."
    ThisModule_Version = "7_03   2022 March 9."  
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
    #   Where possible we base our resources in this program's repostitory
    #   at github. If github basing is not possible or inadequate
    #   we have to use another cloud storage site, eg Youtube, Google drive.
         
    # Program Help/Documentation.    
    Link01 = ("https://github.com/ProfBrockway/ScreeningTest/blob/" 
              "main/Documentation_screeningtest.py.pdf")
    # Project Folder at Github.
    Link02 = "https://github.com/ProfBrockway/ScreeningTest"
    # Where to report a bug.
    Link04 = "https://github.com/ProfBrockway/ScreeningTest/issues"
    # Link to this programs source code
    Link06 = "https://github.com/ProfBrockway/ScreeningTest/blob/main/screeningtest.py"
    # App documentation video.
    Link20 = "https://youtu.be/EuKDZNXmOU8"
    
    # Filenames.
    DataTable_Download_FileName_xcl = "ScreeningTestDataFrame.xlsx"
    DataTable_Download_FileName_CSV = "ScreeningTestDataFrame.csv"
    Report_Download_FileName = "ScreeningTestReport.txt"
    Fig1_Download_FileName = "ScreeningTestFig1.html"
    Fig2_Download_FileName = "ScreeningTestFig2.html"
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

  
    # THE RANGE OF PREVALENCES
    # A list to contain all the Prevs we will test and graph.
    PrevList = list([])
    PrevStart = None       # Input by the user.
    PrevEnd = None         # Input by the user.
    PrevInt = None         # Input by the user.

    # Statistics extracted and the start and end of the range of prevalences.
    PrevStartFPR = None
    PrevEndFPR = None
    PrevStartFNR = None
    PrevEndFNR = None 

    # Statistics extracted at the prevalence of interest.
    PrevInt_FPPercent = None
    PrevInt_FNPercent = None
    PrevInt_PPV = None
    PrevInt_NPV = None
    PrevInt_TP = None
    PrevInt_FP = None
    PrevInt_TN = None
    PrevInt_FN = None  

    # The report title input by the user.
    UsersReportAnnotation = None
    
    # THE DATATABLE
    # The DataTable is a pandas dataframe (data table) to store our results.
    # - This program tests a range of values for prevalences [0 , 1]
    # - Each table row stores the results for a particular 'prevalence'.
    DataTable = pd.DataFrame(
        columns=["Prevalence",
                 "FPPercent",
                 "PPV",
                 "FNPercent",
                 "NPV",
                 "PrevInt",
                 "Sens",
                 "Spec",
                 "TP",
                 "FP",
                 "TN",
                 "FN",
                 "ACC",
                 "Population" 
                ]
                               )

    # SUNDRY GLOBAL VARIABLES
    Fig1 = None
    Plot1 = None
    Fig2 = None
    Plot2 = None
    Msg01 = "Enter the parameters of the medical screening test "\
            "and click 'Plot Now' button."
    
    Plot_Report = None

# End of Global Variables
G = Global_Variables()    # Instantiate our global variables.

def MainLine():
    # Remember this program is rerun by Streamlit every time the GUI is 
    # displayed and the "form run button" is clicked by the user.
    # So we have to keep track of the conversation state.
    #  - We preserve converstation state and other "static" values across 
    #    reinvocations in the Streamlit "Static" dictionary.
    #  - We perform a "one time"  program initialization when the code is
    #    first loaded. 
    #  - On every invocation we perform "every time" initialization.
        
    ConsoleClear()  # Clear the internal IPython console.

    # If this the initial session then create "Static/Persistent" variables.
    if 'Dialog_State' not in S:
        Initialization_Perform_First_Load_Only() # Create Dialog_State etc.
        S.Dialog_State  = 1  # Upgrade state so we don't come back here.

    else:  # We are responding to a session reply from the user.       
        Initialization_Perform_EveryRun()  # Do "every run" initialization.
        
        # Validate and internalize the user's input.
        InputOK = User_Input_Validate_And_Internalize()
        if InputOK == True:
            # Build a table for the efficacies of the screening test across
            # the range of disease prevalences specified by the user.
            Plot_Generate_Data()
            # Plot the table of efficacies of the screening test.
            GUI_Right_Panel_Build()
            
        # NOT the first invocation.    
        else:  # There is an error in the users input. 
           st.error(G.Msg_Current) # Show the error in the right panel.

    # Display the results and wait for next user input.
    GUI_Build_Vertical_Menu()
    return()  # End of function: MainLine.

def Initialization_Perform_EveryRun():
    # Initalize variables for every run.
    # 
    # Alternatives to repeating initialization here are: 
    # (1) Save static/persistant variables in the streamlit "session_state".
    # (2) Initialize in our Global_Variables class (above)
    #     The Global_Variables class is run everytime the app is run.
    #     So it initializes every time streamlit reruns this program.
    #
    # Turns out we don't need any explicit initializations.
    #    It's all done in our global variables class G.
    # However having an "Every Run" initialization function in case
    # it's needed is good practice.
    return()

def Initialization_Perform_First_Load_Only():

    # Initalize rerun variables etc.
    Initialization_Perform_EveryRun()

    # Build the webpage Help menu. 
    # This function contains a Streamlit st.set_page_config statement.
    #  -This must be the FIRST streamlit function executed in the program.
    #  - This must be called only once. Be careful not to issue any Streamlit
    #    commands before this function executes.
    GUI_HelpMenu_Build()
       
    # Static variables are static, persistant and global.  
    Static_Variables_Create() 
       
    S.MsgText = G.Msg01
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
    
    S.MsgText = ""   # Clear the "error" message text.

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
       Msg_Set("Error 1030: Prevalence Of Interest must lie between "  
               "Prevalence Start and Prevalence End.")
       return(False)
 
    # Internalize the users report title.
    G.UsersReportAnnotation =  S.UserReportAnnotation 
    
    # If we fall through here the users input is all valid.
    S.MsgText = G.Msg01    # Reset the "Please enter test specs" message.
    return(True)  # End of function: User_Input_Validate_And_Internalize

def GUI_Build_Vertical_Menu():        # Build the GUI.
    # - Our GUI is a streamlit web page with widgets in a vertical toolbar 
    #   on the left and a plot and display area on the right.
    
    # - We now make the sidebar a single form with a single submit button.
    #   Because we are using the Streamlit a "form" and its form_submit_button,
    #   this program only reruns when you hit the form submit button, NOT 
    #   (as is default behavior) at each widget interaction.
    Form1 = st.sidebar.form(key="Form1", clear_on_submit=False)

    with Form1:

        
        # Create a textbox for displaying instructions and error messages.
        st.text_area(
            key="MsgText",   # Value will be placed in S.MsgText'].
            label="INSTRUCTIONS",
            height=None,
            max_chars=None,
            help="""The instructions box offers instructions and reports errors
                    in input.""",
            on_change=None)
         
        # Add a form submit button.
        # Every "form" must have exactly one form_submit_button.
        st.form_submit_button(
                    label='Plot Now',
                    on_click=PlotNowButton_Click_Event,
                    help="When you have entered the parameters  \r  "
                    "for the calculations click this  \r  "
                    "button to draw your plot.",
                    args=(),
                    kwargs=())
        
        # Create input boxes in the toolbar for our user specifed variables.
        
        # Input the Test Sensitivity.
        st.number_input(
            key="Sens",              # Value will be placed in S.Sens'].
            value=0.99,
            label="Sensitivity",
            min_value=0.00,
            max_value=1.0,
            step=0.01,
            format="%.7f", 
            help="""Enter the test's Sensitivity.    \r
                   A decimal percentage [ 0, 1]""",
            on_change=None)

        # Input The Test Specificity.
        st.number_input(
            key="Spec",          # Value will be placed in S.Spec'].
            value=0.99,
            label="Specificity",
            min_value=0.00,
            max_value=1.0,
            step=0.01,
            format="%.7f",
            help="""Enter the test's Specificity.  
            A decimal percentage [ 0, 1 ]""",
            on_change=None)

        # Input the start of the range of prevalences to be tested.
        st.number_input(
            key="PrevStart",  # Value will be placed in S.PrevStart'].
            value=0.0,
            label="Prevalence Start",
            min_value=0.00,
            max_value=0.99,
            step=0.01,
            format="%.4f",
            help="""Enter the start of the range of prevalence
                to be plotted.  
                A decimal percentage [ 0, 0.99 ]""",
            on_change=None)

        # Input the end of the range of prevalences to be tested.
        st.number_input(
            key="PrevEnd",  # Value will be placed in S.PrevEnd'].
            value=1.0,
            label="Prevalence End",
            min_value=0.00,
            max_value=1.00,
            step=0.01,
            format="%.4f",
            help="""Enter the end of the range of prevalences to be
            plotted.  \rA decimal percentage [ 0.01, 1 ]""",
            on_change=None)

        # Input the prevalence of interest to be highlighted on the plot
        st.number_input(
            key="PrevInt",    # Value will be placed in S.PrevInt'].
            value=0.03,
            label="Prevalence Of Interest",
            min_value=0.00,
            max_value=1.00,
            step=0.01,
            format="%.7f",
            help=("""Enter the 'Prevalence' of interest.   
                  AKA 'Prior Probability Of Infection'.    
                  A decimal percentage  [ 0,  1 ]"""),
            on_change=None)
 
        # Create a textbox user to input the report annotation.
        st.text_area(
            key="UserReportAnnotation",   # Value will be placed in S.MsgText'].
            label="Report Annotation",
            height=None,
            max_chars=None,
            help=("Optional. Enter an annotation for the report on your "
                  "screening test.  \r" 
                  "Type a simple stream of text. Each 'period+Space' will "
                  "start a new line."),
            on_change=None)
        
        # Input the Population Size.
        st.number_input(
            key="PopSize",        # Value will be placed in S.Popsize'].
            value=100,
            label="Population",
            min_value=1,
            max_value=1000,
            step=1,
            format="%i",
            help="""Enter the population.[100,1000].   
            Population does not effect the relative accuract results 
            which are all percentages of population. Changing Population 
            changes only the number of data points and the absolute numbers
            .""",
            on_change=None,
            args=None,
            kwargs=None,
            disabled=False)
        # End of "With Form"
    
 
    return()  # End of function: GUI_Build_Vertical_Menu

def GUI_Right_Panel_Build():  # Put the plot etc in the GUI right panel.
    
    ###########################################################################
    # +++ BUILD THE PLOT REQUESTED BY THE USER AND PLACE IT ON THE GUI.
    
    # Increase the visibility of the Streamlit "full page" icon.
    Plot_Streamlit_FullScreenIcon_Format()
     
    # Build the plot using Plotly graph objects (GO)(not plotly express).
    Plot_Build()    
    
    # Place a report of the results of the simulation on the GUI
    with st.expander("👍 ** REPORT ON YOUR SCREENING TEST**"):
        # Display a Plot Report box on the GUI.
        st.info(Plot_Report_Build(formatfor="streamlit"))  
        
        # Add button to download the report.  
        st.download_button(
            label="👇 Download The Report", 
            data=Plot_Report_Build(formatfor="streamlit"), 
            file_name=G.Report_Download_FileName, 
            mime= "text/txt",
            key="ReportDownloadButton", 
            help="Download the report.") 
    
    
    # Place  Figure 1 on the GUI.
    # - Don't set height or width on the plot or anywhere else. 
    # - Use 'use_container_width' to letStreamlit and Plotly scale everything. 
    #   Otherwise the GUI won't adjust properly to  different size screens.
    st.plotly_chart(G.Fig1, 
                    use_container_width=True, 
                    config={'displayModeBar': True}, # Force plotly toolbar.
                    sharing="streamlit")
    
    # Add button to download Fig1 as an independent interactive hmtl page.  
    PlotAsInteractiveHTML=plotly.io.to_html(G.Fig1)
    st.download_button(
        label="👇 Download Interactive Plot", 
        data=PlotAsInteractiveHTML, 
        file_name=G.Fig1_Download_FileName, 
        mime= "text/html",
        key="Fig1DownloadPlot", 
        help="Download the plot as an independent interact html page.") 
    
    # Place  Figure 2 on the GUI.
    st.plotly_chart(G.Fig2, 
                    use_container_width=True, 
                    config={'displayModeBar': True}, # Force plotly toolbar.
                    sharing="streamlit")

    # Add button to download Fig2 as an independent interactive hmtl page.
    PlotAsInteractiveHTML=plotly.io.to_html(G.Fig2)
    st.download_button(
        label="👇 Download Interactive Plot", 
        data=PlotAsInteractiveHTML, 
        file_name=G.Fig2_Download_FileName, 
        mime= "text/html",
        key="Fig2DownloadPlot", 
        help="Download the plot as an independent interact html page.") 
    
    ###########################################################################
    # +++ SHOW THE DATATABLE.
    
    # Pretty up the dataframe. We use a Pandas Styler object to do this.
    # We don't really need much styling in this
    # program but I put this comment in as a placeholder.
    # Some better features only work in pandas 1.4 which is still too buggy.
    # But they will be great when the new version is stable.
    StylerA = G.DataTable.style\
       .format(
            {  # Format the cells in each column for precision etc.
            "Prevalence": "{:-.4f}",
            "TP": "{:-.4f}",
            "FP": "{:-.4f}",
            "TN": "{:-.4f}",
            "FN": "{:-.4f}",
            "ACC": "{:-.4f}",
            "SENS": "{:-.4f}",
            "SPEC": "{:-.4f}",
            "PPV": "{:-.4f}",
            "FPPercent": "{:-.4f}",
            "NPV": "{:-.4f}",
            "Prevint": "{:-.4f}",
            "FNPercent": "{:-.4f}",
            "Population": "{:-.0f}", # Integer
            })\
     .set_properties(subset=["Prevalence"],**{"background-color":"aquamarine","color":"black"})\
     .set_properties(subset=["FPPercent"],**{"background-color":"red","color":"black"})\
     .set_properties(subset=["FNPercent"],**{"background-color":"pink","color":"black"})\
     .apply(DataFrame_Highlight_PrevInt_Row, axis=1)
    
    with st.expander("🟢 THE DATA TABLE USED FOR THE PLOT FOLLOWS."):
        st.info(
                "The 'Prevalence of interest' row is highlighted.  \r"
                "You can enlarge the table by clicking the 'View full screen' "
                " icon.  \r"
                "'Float' the mouse over the table and the 'View full screen' "
                "icon will appear.")
    
    st.dataframe(data=StylerA, width=None, height=None)

    ###########################################################################
    #  +++ ADD  "DOWNLOAD DATAFRAME" BUTTONS. (CSV or EXCEL options).
    # - The dataframe is converted to a csv file.
    # - That file is downloaded to the browsers download location.
    # - There is no "save as" menu. The file name is hard coded.
    
    DataFrame_CSV = G.DataTable.to_csv().encode('utf-8')
    helpstr = ("The file will be saved in your browser's default download "
              " location on your computer. ")
    col1, col2 = st.columns(2)
    with col1:     
        st.download_button(label="👇 Download The DataFrame To A CSV File", 
                           data=DataFrame_CSV, 
                           file_name=G.DataTable_Download_FileName_CSV, 
                           mime= "text/csv",
                           key="DownloadCSV_Button", 
                           help=helpstr, 
                           on_click=None, 
                           args=None,
                           kwargs=None, 
                           disabled=False)
        
    with col2:    
        # NOTE !! If we use a styler on the grid we can pass that instead
        #         of the dataframe and preserve all stylings in the excel file.
        DataFrameAsExcel = DataFrame_Convert_To_Excel(StylerA)
        st.download_button(label="👇 Download DataFrame To An Excel File",
            data=DataFrameAsExcel ,
            help="In an Excel file any cell highlighting or other "
                 "styling will be preserved.",  
            file_name= G.DataTable_Download_FileName_xcl)   
    
        
    ###########################################################################
    # +++ SHOW A VIDEO DEMONSTRATING THIS PROGRAM.
    #  Github basing of videos does not allow raw address of large files.
    #  Google basing of videos  does not work because it downloads too slowly.
    #  So until I can figure out how to base videos at github we use Youtube.
    st.info("🎬  A VIDEO DEMONSTRATING THIS PROGRAM'S FEATURES.")   
    st.video(G.Link20)
   
    return  # End of function: GUI_Right_Panel_Build

def GUI_HelpMenu_Build():
    # ++++ Set up a typical "About/Help" menu for the webpage.
    # - The set_page_config command can only be used once per run.
    # - The set_page_config command must be the FIRST Streamlit command used.
    # - New line marker \n must be preceeded by at least two blanks to work.
    st.set_page_config  (
     page_title = "Screening Tests.", 
     
     page_icon = "🦡",
     
     layout="centered", # or "wide".
        # 'wide' gives a bigger display. 
        # 'centered' gives a smaller display
        #  Remember that plots and tables etc on the streamlit webpage 
        #  can be "blownup" by the user clicking an "expand" icon.
        #  So don't worry if the normal view is too small.
     
     initial_sidebar_state="auto",
     
     # \r requires two preceeding spaces to work.
     menu_items={ # These appear as the webpage "about" menu items.
     "Get Help  ": G.Link01,
     "Report a bug  ": G.Link04,
     'About': "  \rProgram: "           + G.ThisModule_FileName 
            + "  \rProject:  "          + G.ThisModule_Project
            + "  \rProgram Purpose:  "  + G.ThisModule_Purpose 
            + "  \rAuthor:  "           + G.ThisModule_Author   
            + "  \rContacts:  "         + G.ThisModule_Contact
            + "  \rProgram Version:  "  + G.ThisModule_Version 
            + "  \rProgram Documentation: " 
                 +  f" [Link ➡️]({G.Link01})"  
            + "  \rProgram Source Code:    "  
                 +  f" [Link➡️]({G.Link06})"    
            + "  \rVideo Introducing the Program:    "  
                 +  f" [Link➡️]({G.Link20})"                  
            + "  \rAll Project Files:    "  
                 +  f" [Link➡️]({G.Link02})"     
            + "  \rReport A Bug:    "  
                 +  f" [Link➡️]({G.Link04})"  
               }
                      )
    return()  # End of function: GUI_HelpMenu_Build

def Plot_Generate_Data():
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
        G.PrevList.append(G.PrevList[i] + prev_increment)
        i = i + 1
   
    # Process each of the Prev's in the list of Prev's to be tested.
    # The stats for each prev are calculated and stored in a table row.
    G.DataTable = G.DataTable[0:0] # Clear the DataTable. Retain its structure.
    
    # We will make a note of the false positive and negative rates at the
    # users prevalence of interest.
    G.PrevInt_FPPercent = None
    G.PrevInt_FNPercent = None
    G.PrevInt_PPV = None
    G.PrevInt_NPV = None
    
    # Statistics extracted and the start and end of the range of prevalences.
    G.PrevStartFPR = None
    G.PrevEndFPR = None
    G.PrevStartFNR = None
    G.PrevEndFNR = None 
    
    # Add rows to the DataTable. 
    # We add one row for each prevalance in the range of prevalances.
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
            
        # ACC: The 'General' Accuracy: = ((TP + TN)) / Pop
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
        
        
        # Make a note of the statistics at the prevalence of interest.
        
        # If we are generating the record for the prevalence of interest
        # save the stats for the prevalence of interest for the report.
        if (PrevCurrent >= G.PrevInt) and (G.PrevInt_FPPercent == None ):
            # We are at or near the prevalence of interest.
            G.PrevInt_FPPercent = G.FPPercent # Save the FP percentage.
            G.PrevInt_FNPercent = G.FNPercent   
            G.PrevInt_PPV = G.PPV
            G.PrevInt_NPV = G.NPV
            G.PrevInt_TP= G.TP
            G.PrevInt_FP= G.FP
            G.PrevInt_TN= G.TN
            G.PrevInt_FN= G.FN     
        
        if (PrevCurrent == G.PrevStart) and (G.PrevStartFPR == None ):    
           G.PrevStartFPR = G.FPPercent
           G.PrevStartFNR = G.FNPercent
           
        if PrevCurrent == G.PrevList[-1] and (G.PrevEndFNR == None ):
           G.PrevEndFPR = G.FPPercent
           G.PrevEndFNR = G.FNPercent
        
        # Add the new row to the DataTable.
        G.DataTable = G.DataTable.append(newrow, ignore_index=True)
    # End of 'For each PrevCurrent'
    return # End of function: Plot_Generate_Data

def Plot_Build(): # Create our plot using Plotly Graph Objects.
    # Plotly graph objects (GO) are for building plots "by hand".
    # GO graphing gives more control than graphing with Plotly Express.
    x_hoverformat = ".4f"
    y_hoverformat = ".4f"
    
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
        xhoverformat= x_hoverformat,
        yhoverformat= y_hoverformat,
        line=dict(color="red")      )) 
   
    G.Fig1.add_trace(go.Scatter(
        name="False Negative Percentage",
        text="False Negative Percentage",
        legendrank=2,
        x=G.DataTable["Prevalence"], y=G.DataTable["FNPercent"],
        visible=True,
        mode="lines",
        xhoverformat= x_hoverformat,
        yhoverformat= y_hoverformat,
        line=dict(color="blue")  ))     

    G.Fig1.add_trace(go.Scatter(
        name="Positive Predictive Value",   
        text="Positive Predictive Value",   
        legendrank=3,
        x=G.DataTable["Prevalence"], y=G.DataTable["PPV"], 
        visible="legendonly",
        mode="lines",
        xhoverformat= x_hoverformat,
        yhoverformat= y_hoverformat,
        line=dict(color="green"  )   ))
  
    G.Fig1.add_trace(go.Scatter(
        name="Negative Predictive Values",
        text="Negative Predictive Values",
        legendrank=4,
        x=G.DataTable["Prevalence"], y=G.DataTable["NPV"], 
        visible="legendonly",
        mode="lines",
        xhoverformat= x_hoverformat,
        yhoverformat= y_hoverformat,
        line=dict(color="magenta")  ))
    
    G.Fig1.add_trace(go.Scatter(
        name="General Accuracy",
        text="General Accuracy",
        legendrank=9,
        x=G.DataTable["Prevalence"], y=G.DataTable["ACC"],
        visible="legendonly",
        mode="lines",
        xhoverformat= x_hoverformat,
        yhoverformat= y_hoverformat,
        line=dict(color="orange")  ))
    
    # Adjust titles, grid, font etc.
    PlotTitle = "<b>Screening Test: Accuracy Percentages"
    G.Fig1.update_layout(
        title=PlotTitle,
        title_x=0.4,
        xaxis_title="<b>Disease Prevalence In Population",
        yaxis_title="<b>Response Of The Screening Test")
    G.Fig1.update_xaxes(showgrid=True,gridcolor="lightgray")
    G.Fig1.update_yaxes(showgrid=True,gridcolor="lightgray")
    # We MUST let the plot autosize so that it will best fit different
    # size screens. 
    G.Fig1.update_layout(autosize=True, width=None, height=None) #800*1100
    G.Fig1.layout.plot_bgcolor = "white"
    #G.Fig1.layout.margin = dict(t=5, b=5, l=0, r=0)
        
    # Adjust the hover text aka "mouseover" text.
    # Show hover values for all visible lines (aka traces).
    G.Fig1.update_layout(hovermode="x") # "x", "x unified" or "closest"
    # Show vertical and horizontal hover axes intersect lines.
    G.Fig1.update_xaxes(showspikes=True, spikecolor="green",spikethickness=1, 
                        spikesnap="cursor", spikemode="across")
    G.Fig1.update_yaxes(showspikes=True, spikecolor="green", spikethickness=1)
    # Specify what is shown on each hovertext line.
    # https://plotly.com/python/hover-text-and-formatting/#advanced-hover-template
    # HT=("<br>" + "At Prevalence=%{x:.4f},  " + "y=%{y:.4f}") 
    HT=("<br>" + "Prev=%{x}, " + "y=%{y}") 
    G.Fig1.update_traces(hovertemplate=HT,hoverlabel=dict())
    G.Fig1.update_traces(hoverlabel=dict(namelength=50)) #Suppress floating part. 
    # Adjust the hovertext font.  
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
    layoutojb=go.Layout(
        annotations=[
            go.layout.Annotation(
                text=Plot_Report_Build(formatfor="html"),
                align="left",
                showarrow=False,
                xref="paper",
                yref="paper",
                # x=0.5,
                # y=0.8,
                x= 1.00, xanchor = "left",
                y= 0.05, yanchor = "bottom",
                bordercolor="black",
                borderwidth=1)])
    G.Fig1.update_layout(layoutojb)
    # G.Fig1.add_annotation(
    #     text=Plot_Report_Build(formatfor="html"), 
    #         align="left",
    #         showarrow=False,
    #         xref="paper", yref="paper",
    #         x= 1.0, xanchor = "left",
    #         y= 0.25, yanchor = "bottom",
    #         bordercolor="black", borderwidth=0)
   

    
    ###########################################################################
    #  CREATE FIGURE 2:  THE ABSOLUTE NUMBER OF POSITIVES AND NEGATIVES
    ###########################################################################
         
    G.Fig2 = go.Figure() # Create an empty Plotly figure.
    
    G.Fig2.add_trace(go.Scatter(
        name="True Positive",
        text="True Positive",
        legendrank=6,
        x=G.DataTable["Prevalence"], y=G.DataTable["TP"], 
        visible=True,
        mode="lines",
        xhoverformat= x_hoverformat,
        yhoverformat= y_hoverformat,
        line=dict(color="black")  ))
    
    G.Fig2.add_trace(go.Scatter(
        name="False Positive",
        text="False Positive",
        legendrank=6,
        x=G.DataTable["Prevalence"], y=G.DataTable["FP"], 
        visible="legendonly",
        mode="lines",
        xhoverformat= x_hoverformat,
        yhoverformat= y_hoverformat,
        line=dict(color="black")  ))

    G.Fig2.add_trace(go.Scatter(
        name="True Negative",
        text="True Negative",
        legendrank=8,
        x=G.DataTable["Prevalence"], y=G.DataTable["TN"], 
        visible=True,
        xhoverformat= x_hoverformat,
        yhoverformat= y_hoverformat,
        line=dict(color="peru" ) ))    

    G.Fig2.add_trace(go.Scatter(
        name="False Negative",
        text="False Negative",
        legendrank=8,
        x=G.DataTable["Prevalence"], y=G.DataTable["FN"], 
        visible="legendonly",
        xhoverformat= x_hoverformat,
        yhoverformat= y_hoverformat,
        line=dict(color="peru" ) ))
    
    PlotTitle = "<b>Screening Test:   Claimed Absolute Numbers."
    
    G.Fig2.update_layout(
        title=PlotTitle,
        title_x=0.4,
        xaxis_title="<b>Disease Prevalence In Population",
        yaxis_title="<b>Claimed Absolute Number Of Response Variable")
    
    G.Fig2.update_layout(xaxis = dict(tickmode = 'linear',
                         tick0 = G.PrevStart, dtick = XtickIncrement))
  
    return() # End of function:   Plot_Build()

def Plot_Report_Build(formatfor="regular"):

    if  formatfor == "streamlit": 
        ind = " -- " 
        eol =   ".  \r"  # ". \u000D"
    elif formatfor == "html":
        ind = " - "
        eol = ".  \r"   
    else: 
        ind = " - "
        eol = ".  \r"
        
    header = "**REPORT ON YOUR SCREENING TEST** "
    if G.UsersReportAnnotation == None \
       or G.UsersReportAnnotation == ""  \
       or G.UsersReportAnnotation.isspace():
       pass    
    else:
        # User has supplied a report annotation. Edit it to create new line
        # after each period.
        G.UsersReportAnnotation=G.UsersReportAnnotation.replace(". ",".  \r") 
        header = header + "  \n" + G.UsersReportAnnotation 
                    
    G.Plot_Report = str(
       header  + "  \n   \n"                                                 +
            "\n** Inputs specifying the simulation. **   \n"                 +
       ind + "In this simulation the disease prevalence varies "             +
             f"from {G.PrevStart:.5f} to {G.PrevEnd:.5f}.   \n"              +
       ind + f"Test Sensitivity = {G.Sens:.4f}.   \n"                        +
       ind + f"Test Specificity = {G.Spec:.4f}.   \n"                        +
       ind + f"Plot Prevalence Start = {G.PrevStart:.5f}.   \n"              +
       ind + f"Plot Prevalence End = {G.PrevEnd:.5f}.   \n"                  +
       ind + f"Population = {G.PopSize:.0f}.   \n"                           +
             "\n** The range of false results. **   \n"                      +
       ind + "The false positive rate varies "                               +
              f"from {G.PrevStartFPR:.5f} to {G.PrevEndFPR:.5f}.   \n"       +
       ind + "The false negative rate varies "                               +
             f"from {G.PrevStartFNR:.5f} to {G.PrevEndFNR:.5f}.   \n"        + 
             f"\n** At The Prevalence Of Interest = {G.PrevInt:.6f}. **   \n" + 
       ind + f"About {G.PrevInt_FPPercent:.2f} "                             +
              "of all positives are false.  \n"                               + 
       ind + f"About {G.PrevInt_FNPercent:.2f} "                             + 
              "of all negatives are false.  \n"                              +      
       ind + f"Positive Predictive Value (PPV) = {G.PrevInt_PPV :.4f}.   \n" +
       ind + f"Negative Predictive Value (NPV) = {G.PrevInt_NPV :.4f}.   \n" +
       ind + f"Claimed True Positives = {G.PrevInt_TP:.2f}.    \n"           +
       ind + f"Claimed False Positives = {G.PrevInt_FP:.2f}.   \n"           +
       ind + f"Claimed True Negatives = {G.PrevInt_TN:.2f}.    \n"           +
       ind + f"Claimed False Negatives = {G.PrevInt_FN:.2f}.   \n"                             
                       ) 
    
    if formatfor == "html":  
       G.Plot_Report = str(""                                               +   
       "**Inputs**<br>"                                                     +
       ind + "Disease prevalence:"                                          +
             f"from {G.PrevStart:.5f} to {G.PrevEnd:.5f}.<br>"              +
       ind + f"Test Sensitivity = {G.Sens:.4f}.<br>"                        +
       ind + f"Test Specificity = {G.Spec:.4f}.<br>"                        +
       ind + f"Population = {G.PopSize:.0f}.<br>"                           +
       ind + f"Prevalence of Interest = {G.PrevInt:.5f}.")               
        
    return(G.Plot_Report)   # End of function: Plot_Report_Build


def Plot_Streamlit_FullScreenIcon_Format():
    # This function increases the visibility of the Streamlit
    # 'full page' icon. It injects css code using markdown.
    css = """
         button[title="View fullscreen"] 
         {background-color: #004170cc; left: 2; color: white; }
         button[title="View fullscreen"]:hover 
         {background-color: #004170; color: white; } """
    st.markdown( "<style>" + css + "</styles>", unsafe_allow_html=True)
    return() # End of function: Plot_Streamlit_FullScreenIcon_Format
    

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
    # Format text for our output message text box.
    FormattedText = TextString
    ErrStr = TextString[0:5].upper()  
    if ErrStr == "ERROR": # If this is an error message append an error prefix.
       FormattedText = ("❌  There is an error in your input.  \r"
                       f"{FormattedText}  Please correct and try again.")
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

def DataFrame_Convert_To_Excel(df):
    sheetname = "ScreeningTest"
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")
    df.to_excel(writer, index=True, sheet_name=sheetname)
    workbook = writer.book
    worksheet = writer.sheets[sheetname]
    format1 = workbook.add_format({"num_format": '00.00000'}) 
    worksheet.set_column("A:A", None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return (processed_data)

def DataFrame_Highlight_PrevInt_Row(RowI):
    Formatter = "" 
    if RowI.FPPercent == G.PrevInt_FPPercent:
        Formatter=["background-color:yellow; color:black;"  for col in RowI]
    else:
        Formatter=[";"  for col in RowI] # Leave prevailing formatting.
    return(Formatter)

def Static_Variables_Create():         
    # +++ CREATE STATIC VARIABLES.
    # Streamlit reloads the app everytime the user replys to the GUI.
    # We therefore have to store any variables needed across invocations
    # in the Streamlit "Static" Storage.
    #
    # STATIC VARIABLES:
    #   - Static variables are static (preserved) between sessions.    
    #   - Static variables are stored and created by Streamlit in the Streamlit
    #     "session_state" dictionary.
    #   - Static variables are effectively global within the app.
    #   - Static variables are created in two ways:
    #       (1) Explicitly: 
    #         - Declared using the Streamlit "session_state" method.
    #           - Eg:  st.session_state['Display_Count'] = 0
    #         - In our case the st.session_State is abbreviated to S.
    #            - Eg: S.Input_SSN = 0 (import session_state as S).
    #      (2) Implicitly Using The Streamlit Widget key= keyword.
    #         - A Streamlit widget with a key=namex automatically
    #           creates a static variable called namex in the Streamlit Static
    #           dictionaryy.
    #            - Any change in the linked widget in th GUI  will
    #              automatically update the linked static variable.
    #            - Any change in the static variable will automatically 
    #              update the linked widget in the GUI
    #      - The python 'type' of linked static variables are specifed by the
    #        linked widget's "format=" parameter.
    #      - Eg of a Linked persistent variable.
    #            st.number_input(label=:Enter Age", key="Age")
    S.Dialog_State = 0    # Create session Dialog_State variable.
    return() # End of function: Static_Variables_Create



MainLine()   # Start this program.


