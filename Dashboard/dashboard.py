#Importing the libraries
# We will be using pandas for dataset manipulation
# numpy - for mathematical reasons like rounding off
# plotly to plt the graphs
# streamlit for sidebar 
# streamlit_lottie for animations
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import requests
from streamlit_lottie import st_lottie

#Reading the placement.csv dataset into data
data = pd.read_csv(r"placement.csv")

#Now we will be replacing the M with Male and F with Female in gender column for prettier dataset
data['gender']=data['gender'].replace('M','Male')
data['gender']=data['gender'].replace('F','Female')
#Now we will be replacing the Comm&Mgmt with Commerce and Management and  Scie&Tech with Science and Technology in degree column for prettier dataset
data['degree_t']=data['degree_t'].replace('Comm&Mgmt','Commerce and Management')
data['degree_t']=data['degree_t'].replace('Sci&Tech','Science and Technology')
#Now we will be replacing the Mkt&HR' with Marketing and HR and Mkt&Fin with Marketing and Finance in specialisation column for prettier dataset
data['specialistion']=data['specialisation'].replace('Mkt&HR','Marketing and HR')
data['specialistion']=data['specialisation'].replace('Mkt&Fin','Marketing and Finance')


#This helps us to set the page details that appear on the tab
st.set_page_config(
    page_title="Placement Details", #The page title, shown in the browser tab.(should be Placement Details)
    initial_sidebar_state="auto", #The way sidebar should start out. Auto shows it in desktop.
    page_icon=":computer:", #The page favicon. Use the computer emoji
    layout="wide", #The way page content should be laid out. "wide" uses the entire screen.
    menu_items={ #Configure the menu that appears on the top-right side of this app.
            'About': 'https://www.linkedin.com/in/harsh-kashyap-79b87b193/', #A markdown string to show in the About dialog. Used my linkedIn id
     }
)

# Sidebar Options which can be changed to filter out the result
st.sidebar.header("Options")
#Multiple options to be displayed
branch = st.sidebar.multiselect(
    "Select the Stream:", #Heading of the particular sidebar
    options=data["hsc_s"].unique(), #All the availaible options
    default=data["hsc_s"].unique() #Initially show user with all the option present
)
gender = st.sidebar.multiselect(
    "Select the Gender:", #Heading of the particular sidebar
    options=data["gender"].unique(),#All the availaible options
    default=data["gender"].unique() #Initially show user with all the option present
)
degree = st.sidebar.multiselect(
    "Select the Degree:",#Heading of the particular sidebar
    options=data["degree_t"].unique(),#All the availaible options
    default=data["degree_t"].unique()#Initially show user with all the option present
)

place = st.sidebar.multiselect(
    "Select the Status:",#Heading of the particular sidebar
    options=data["status"].unique(),#All the availaible options
    default=data["status"].unique()#Initially show user with all the option present
)
special = st.sidebar.multiselect(
    "Select the Specialisation:",#Heading of the particular sidebar
    options=data["specialisation"].unique(),#All the availaible options
    default=data["specialisation"].unique()#Initially show user with all the option present
)

#Query the columns of a DataFrame with a boolean expression.
data_selection = data.query(
    "hsc_s == @branch & gender == @gender & degree_t == @degree & status == @place & specialisation == @special"
)
#Example hsc_s == @branch
#Checks if which parameters in hsc_s which is named as branch in sidebar is checked or not and display results accordingly
def load_lottieurl(url: str):
    r = requests.get(url) #Make a request to a web page, and return the status code:
    if r.status_code != 200: #200 is the HTTP status code for "OK", a successful response.
        return None
    return r.json() #return the animated gif


# Main Page
st.title(":computer: Placements Visualisation") #Title heading of the page
st.markdown("##") #Markdown or line breaker

left_column, right_column = st.columns(2) #Columns divided into two parts
with left_column:
    dashboard1 = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_q5qeoo3q.json") #get the animated gif from file
    st_lottie(dashboard1, key="Dashboard1", height=400) #change the size to height 400
with right_column:
    dashboard2 = load_lottieurl("https://assets10.lottiefiles.com/private_files/lf30_fqygznk9.json") #get the animated gif from file
    st_lottie(dashboard2, key="Dashboard2", height=400) #change the size to height 400


st.markdown("""---""")  #Markdown or line breaker
average_marks1 = np.round(data_selection["ssc_p"].mean(),2) #Calculate the average of the selected data and round off to 2 digit places
average_marks2 = np.round(data_selection["hsc_p"].mean(),2) #Calculate the average of the selected data and round off to 2 digit places
average_marks3 = np.round(data_selection["degree_p"].mean(),2) #Calculate the average of the selected data and round off to 2 digit places
average_marks4 = np.round(data_selection["etest_p"].mean(),2) #Calculate the average of the selected data and round off to 2 digit places
average_marks5 = np.round(data_selection["mba_p"].mean(),2) #Calculate the average of the selected data and round off to 2 digit places
average_marks6 = np.round(data_selection["salary"].mean(),2) #Calculate the average of the selected data and round off to 2 digit places
left_column, mid_column, right_column = st.columns(3)  #Columns divided into three parts
with left_column:
    st.subheader("Average Marks in 10th:") #Header of average marks scored in 10th
    st.subheader(str(average_marks1)) #print the average marks
with mid_column:
    st.subheader("Average Marks in 12th:")  #Header of average marks scored in 12th
    st.subheader(str(average_marks2)) #print the average marks
with right_column:
    st.subheader("Average Marks in Graduation:")  #Header of average marks scored in Graduation
    st.subheader(str(average_marks3)) #print the average marks
st.markdown("""---""") #Markdown or line breaker

left_column, mid_column, right_column = st.columns(3) #Columns divided into three parts
with left_column:
    st.subheader("Average Marks in GRE:")  #Header of average marks scored in GRE
    st.subheader(str(average_marks4)) #print the average marks
with mid_column:
    st.subheader("Average Marks in MBA:")  #Header of average marks scored in MBA
    st.subheader(str(average_marks5)) #print the average marks
with right_column:
    st.subheader("Average Salary (yearly):") #Header of average marks scored in Salary
    st.subheader(str('\u20B9')+" "+str(average_marks6)) #print the average marks
st.markdown("""---""")


#Count No. of male and female 
gendercount=data_selection['gender'].value_counts().sort_index(axis=0)

#Pie Graph
fig_pie1 = px.pie(
    values=gendercount.values, #No. of males and females
    names=gendercount.index, #Male and Female label
    title="<b>Selected Gender</b>",
    color_discrete_sequence=px.colors.cyclical.Twilight #color in pie chart
)
#Count No. of placed and not placed
placedcount=data_selection['status'].value_counts().sort_index(axis=0)
#Pie Graph
fig_pie2 = px.pie(
    values=placedcount.values, #No. of placed and not placed
    names=placedcount.index, #Placed and Not Placed label
    title="<b>Placement Status</b>",
)
left_column, right_column = st.columns(2) #Columns divided into two parts
left_column.plotly_chart(fig_pie1,use_container_width=True)  #piechart in left side
right_column.plotly_chart(fig_pie2, use_container_width=True) #piechart in right side
st.markdown("""---""") #dashed line

#scatter plot for 10th vs 12th with Placed Status
marks10=data_selection[['ssc_p','hsc_p','status']]
#column name of dataset to be changed
marks10.columns=["10th Marks","12th Marks","Job Status"]
fig_scatter1 = px.scatter(
    marks10, #marks10 dataset
    x='10th Marks', #x axis has 10th marks
    y="12th Marks", #y axis has 12th marks
    color='Job Status',#filter has placement status
    orientation="h",
    title="<b>Marks 10th VS 12th (Consistency)</b>", #title
)
#remove the background of the back label
fig_scatter1.update_layout(
    plot_bgcolor="rgba(0,0,0,0)"
)

#scatter plot for Graduation Marks and MBA marks showing the relation between them
marksMBA=data_selection[['degree_p','mba_p','salary']]
#column name of dataset to be changed
marksMBA.columns=["Degree Marks","MBA Marks","Salary"]
fig_scatter2 = px.scatter(
    marksMBA, #marksMBA dataset
    x='Degree Marks', #x axis has Graduation marks
    y="MBA Marks", #y axis has MBA marks
    color='Salary', #filter has Salary amount
    orientation="h",
    title="<b>Marks Graduation VS MBA (Consistency)</b>",
)
#remove the background of the back label
fig_scatter2.update_layout(
    plot_bgcolor="rgba(0,0,0,0)"
)
left_column, right_column = st.columns(2)  #column has been divided into 2 parts
left_column.plotly_chart(fig_scatter1,use_container_width=True) #Keep the 10th vs 12th on the left side
right_column.plotly_chart(fig_scatter2, use_container_width=True) #Keep the Graduation Vs 12th Graph on right side
st.markdown("""---""") #dash line seperator


#change the column name hsc_s to stream
stream=data_selection.rename(columns={"hsc_s":"Stream"})
stream=data_selection.groupby(by='hsc_s').mean()  #group the mean by stream Science, commerce or Arts
stream.columns=["sl","10th Marks","12th Marks","Graduation Marks","GRE Marks","MBA Marks","Salary"] #rename the column names
#creating a bar graph
fig_bar1 = px.bar(
    stream, #dataset of the average marks for each branch
    y="10th Marks", #10th marks
    x=stream.index, #the stream chosen
    orientation="v",
    title="<b>10th Marks for Various Streams</b>",
    color_discrete_sequence=["cyan"] * len(stream), #color sequence will change depending on length of stream
)
#remove the background of the back label
fig_bar1.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",  #transparent
    xaxis=(dict(showgrid=False)) #dont show the grid
)
#creating a bar graph
fig_bar2 = px.bar(
    stream, #dataset of the average marks for each branch
    y="12th Marks", #12th marks
    x=stream.index, #the stream chosen
    orientation="v",
    title="<b>12th Marks for Various Streams</b>",
    color_discrete_sequence=["brown"] * len(stream), #color sequence will change depending on length of stream
)
#remove the background of the back label
fig_bar2.update_layout(
    plot_bgcolor="rgba(0,0,0,0)", #transparent
    xaxis=(dict(showgrid=False))  #dont show the grid
)
#creating a bar graph
fig_bar3 = px.bar(
    stream, #dataset of the average marks for each branch
    y="Graduation Marks", #Graduation marks
    x=stream.index,  #the stream chosen
    orientation="v",
    title="<b>Graduation Marks for Various Streams</b>",
    color_discrete_sequence=["pink"] * len(stream) #color sequence will change depending on length of stream
)
#remove the background of the back label
fig_bar3.update_layout(
    plot_bgcolor="rgba(0,0,0,0)", #rgba means transparent
    xaxis=(dict(showgrid=False)) #dont show the grid
)
left_column, mid_column, right_column = st.columns(3) #column has been divided into 3 parts
left_column.plotly_chart(fig_bar1,use_container_width=True) #plotting a bar graph on left side of screen 
mid_column.plotly_chart(fig_bar2,use_container_width=True) #plotting a bar graph on middle side of screen 
right_column.plotly_chart(fig_bar3, use_container_width=True) #plotting a bar graph on right side of screen 
st.markdown("##") #dashed line

#creating a bar graph
fig_bar4 = px.bar(
    stream, #dataset of the average marks for each branch
    y="GRE Marks", #GRE marks
    x=stream.index, #the stream chosen
    orientation="v",
    title="<b>GRE Marks for Various Streams</b>",
    color_discrete_sequence=["Green"] * len(stream), #color sequence will change depending on length of stream
)
#remove the background of the back label
fig_bar4.update_layout(
    plot_bgcolor="rgba(0,0,0,0)", #rgba means transparent
    xaxis=(dict(showgrid=False)) #dont show the grid
)
#creating a bar graph
fig_bar5 = px.bar(
    stream, #dataset of the average marks for each branch
    y="MBA Marks", #MBA marks
    x=stream.index, #the stream chosen
    orientation="v",
    title="<b>MBA Marks for Various Streams</b>",
    color_discrete_sequence=["Violet"] * len(stream),  #color sequence will change depending on length of stream
)
#remove the background of the back label
fig_bar5.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",  #rgba means transparent
    xaxis=(dict(showgrid=False)) #dont show the grid
)
#creating a bar graph
fig_bar6 = px.bar(
    stream, #dataset of the average marks for each branch
    y="Salary", #Salary
    x=stream.index, #the stream chosen
    orientation="v",
    title="<b>Salary for Various Streams</b>",
    color_discrete_sequence=["Yellow"] * len(stream), #color sequence will change depending on length of stream
)
#remove the background of the back label
fig_bar6.update_layout(
    plot_bgcolor="rgba(0,0,0,0)", #rgba means transparent
    xaxis=(dict(showgrid=False)) #dont show the grid
)
left_column, mid_column, right_column = st.columns(3) #column has been divided into 3 parts
left_column.plotly_chart(fig_bar4,use_container_width=True) #plotting a bar graph on left side of screen 
mid_column.plotly_chart(fig_bar5,use_container_width=True)#plotting a bar graph on middle side of screen 
right_column.plotly_chart(fig_bar6, use_container_width=True) #plotting a bar graph on right side of screen 
st.markdown("""---""") #dashed line

gD=data_selection.sort_values(by="salary") #sort sdata by salary
gD=pd.DataFrame(gD.dropna()) #drop NAN values
gD.reset_index(drop=True, inplace=True) #reset the index 
st.subheader("Gender Disparity in Pay Scale") #Header
#plot a line graph
fig_line = px.line(
    gD,  #dataset is the filtered gD created above
    x = gD.index,  #index of the gD
    y = "salary", #salary which is sorted
    color = "gender", #two graphs for eavh gender
    width=1400, #width of the chart
    height=750, #height of the chart
)
#remove the background of the back label
fig_line.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",  #rgba means transparent
    xaxis=(dict(showgrid=False)) #dont show the grid
)
#plot the chart
st.plotly_chart(fig_line, use_container_width=True)
st.markdown("""---""")
#to remove the footer and header of streamlit
hide_st_style = """
             <style>
             footer {visibility: hidden;}
             header {visibility: hidden;}
             </style>
             """
st.markdown(hide_st_style, unsafe_allow_html=True) #to hide the footer elements of default

footer = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_tjbhujef.json") #thank you gif
st_lottie(footer, key="Footer",height=300) #gif 
st.header("Made with Love By Harsh Kashyap") #bnottom tag