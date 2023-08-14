# Web App with Streamlit

# Author: Reza Masoudian, Created on July 25, 2023

# ---------------------------------------------------------
import pandas as pd
import streamlit as st
from pyxlsb import open_workbook as open_xlsb
import numpy as np
import plotly.graph_objects as go
import os
print(os.getcwd())

os.system('pip install --upgrade pip')

# --------------------------------------------------------
# # Defining functions: Loading Data
# @st.cache
# def load_and_save_data(xlsb_file, output_folder):
#     from openpyxl import load_workbook
#     df = [] # list

#     with open_xlsb(xlsb_file) as wb:
#         with wb.get_sheet(1) as sheet: # 1 is the index of the sheet
#             for row in sheet.rows():
#                 df.append([item.v for item in row]) # getting value from cell item  

#     title= df[1]
#     print(title)

#     #---------------------------------------------
#     # Initializing the dictionary
#     dict_of_lists = {}
#     current_list_name = ""

#     for i in range(len(title)):
#         if title[i] is not None:
#             # This is a new list
#             current_list_name = title[i]
#             dict_of_lists[current_list_name] = []
#             dict_of_lists[current_list_name].append(i)
#         elif current_list_name:
#             # Add index to the current list
#             dict_of_lists[current_list_name].append(i)

#     # Print the resulting dictionary
#     for k, v in dict_of_lists.items():
#         print(f"{k}: {v}")

#     # -----------------------------------------------------

#     header = df[2] # Get the header from the third row as a list
#     header[0] = 'Site'

#     # Identify the first None component in the first column
#     end_component = next((i for i, v in enumerate((item[0] for item in df[3:]), 3) if v is None), None)
#     df = pd.DataFrame(df[3:end_component], columns=header) # Create DataFrame excluding header

#     tables_dict = {}

#     # split columns
#     for k, v in dict_of_lists.items():
#         column_names = ['Site'] + [header[i] for i in v] # Select column names based on indices
#         tables_dict[k] = df[column_names] # Assign dataframe subset to dict

#     if tables_dict:
#         # rename first key in dictionary
#         first_key = list(tables_dict.keys())[0]
#         tables_dict["Types of Functional Locations"] = tables_dict.pop(first_key)
#     else:
#         print("The dictionary is empty.")

#     # create output folder if it doesn't exist
#     os.makedirs(output_folder, exist_ok=True)

#     # save tables to .csv files
#     for table_name, table_df in tables_dict.items():
#         # replace "/" with "_" in table names
#         safe_table_name = table_name.replace("/", "_")
#         safe_table_name = safe_table_name.replace(" ", "_")
#         safe_table_name = safe_table_name.replace("(", "_")
#         safe_table_name = safe_table_name.replace(")", "_")
#         safe_table_name = safe_table_name.replace("'", "_")

#         table_df.to_csv(f'{output_folder}/{safe_table_name}.csv', index=False)


#     # Cleaning the empty columns of "FL Catg N (NAVI) UsrSt Checks.csv":
#     new_t = pd.read_csv(f'{output_folder}/FL_Catg_N__NAVI__UsrSt_Checks.csv')
#     new_t = new_t.dropna(how='all', axis=1)
#     new_t.to_csv(f"{output_folder}/FL_Catg_N__NAVI__UsrSt_Checks.csv" , index=False) # f: likes the f we already used in oother scripts!
#     # Calling the function:
#     load_and_save_data("6172-All FLs Full Analysis for Struct_Quality JG Rev5_Chart.xlsb", "Data_Streamlit")

# -------------------------
# -------------------------
# Merging dataframes

# ----------- 'PU_Child_PG_and_WC_Data_Orig_Chks.csv'
dir = './Data_Streamlit'

table_path_1 = os.path.join(dir, 'Plnr_Group_Data_Origin_Checks.csv')
table_1 = pd.read_csv(table_path_1)

table_path_2 = os.path.join(dir, 'Work_Center_Data_Origin_Checks.csv')
table_2 = pd.read_csv(table_path_2)

table_path_3 = os.path.join(dir, 'Misc.csv')
table_3 = pd.read_csv(table_path_3)

# First merge table_1 and table_2
merged_12 = table_1.merge(table_2, how='left', on='Site')
# Then merge the result with table_3
Merged_Output = merged_12.merge(table_3, how='left', on='Site')

# Specify a file name for the output
output_file = os.path.join(dir, 'PU_Child_PG_and_WC_Data_Orig_Chks.csv')
Merged_Output.to_csv(output_file, index=False)

# -------------------- Usr_Stat_AUCN_SOLD_DCOM_and_Sys_S
# the method of reading dataframe is  different of the previous part, just for education
table_1 = pd.read_csv('./Data_Streamlit/PU_Child_UsrSt__Asset_Under_Const___AUCN__Chks.csv')
table_2 = pd.read_csv('./Data_Streamlit/PU_Child_UsrSt__Not_on_Site___Decom___SOLD_DCOM__Chks.csv')
table_3 = pd.read_csv('./Data_Streamlit/PU_Child_System_Status_Comparisons.csv')
merged_12 = table_1.merge(table_2, how='left', on='Site')
Merged_Output = merged_12.merge(table_3, how='left', on='Site')
output_file = os.path.join(dir, 'Usr_Stat_AUCN_SOLD_DCOM_and_Sys_S.csv')
Merged_Output.to_csv(output_file, index=False)
# --------------------------------------------------------------------
# --------------------------------------------------------------------


st.image('./logo.png', use_column_width= True)


# Dashboard Features
#st.sidebar.image('./logo_dashboard.png', use_column_width= True)

st.sidebar.header('Input Parameters')


# Directory where the dataframes are stored
dir = './Data_Streamlit'

# Get a list of the dataframe names
df_names = os.listdir(dir)

# Remove any non .csv files if present
df_names = [df for df in df_names if df.endswith('.csv')]

# Sidebar selectbox for dataframe selection
selected_df_name = st.sidebar.selectbox('Select a dataframe', df_names)

#--------- Tables

# Color function
def create_custom_table(df, header_fill_color='#0F123D', header_font_color='#F4BA41', header_font_size=11, header_alignment= 'center', 
                        header_line_color='#118DFF', header_line_width=2,
                        cell_fill_color='#0F123D', cell_font_color='#04CEDC', cell_font_size=10, cell_alignment= 'center', cell_line_color='#118DFF', cell_line_width=1):
    import plotly.graph_objects as go
    
    # Convert the dataframe to a list of lists
    df_values = [df[col].tolist() for col in df.columns]

    # Create a table
    fig = go.Figure(data=[go.Table(
        header=dict(values=df.columns.tolist(),
                    fill_color=header_fill_color,
                    align=header_alignment,
                    line=dict(color=header_line_color, width=header_line_width),
                    font=dict(color=header_font_color, size=header_font_size)),
        cells=dict(values=df_values,
                   fill_color=cell_fill_color,
                   align=cell_alignment,
                   line=dict(color=cell_line_color, width=cell_line_width),
                   font=dict(color=cell_font_color, size=cell_font_size)))
    ])
    
    return fig

#-------- Diagrams
#------------------------

def plot_donut_chart(df, col_indices=[2, 4], row_index=0, colors=['#f54291', '#542ad1'], legend_font_color='#000000', legend_font_size=12, text_color='#000000', text_font_size=14, textinfo='label+percent', textposition='outside', marker=dict(colors=['#f54291', '#542ad1'], line=dict(color='#000000', width=2)), 
                   pull=[0.1, 0.1], rotation=90, hole=0.4):

    # Get the column names as labels and first row values as sizes
    labels = df.columns[col_indices[0]:col_indices[-1]+1]
    sizes = df.iloc[row_index, col_indices[0]:col_indices[-1]+1]

    # Create donut chart
    fig = go.Figure(data=[go.Pie(labels=labels, 
                                 values=sizes, 
                                 textinfo=textinfo,
                                 textposition=textposition,
                                 marker=marker,
                                 pull=pull,
                                 rotation=rotation,
                                 hole=hole)])  # Added 'hole' parameter

    # Update the font size and color of the text
    fig.update_traces(textfont_size=text_font_size, textfont_color=text_color)

    # Update legend font color and size
    fig.update_layout(
        legend=dict(
            font=dict(
                color=legend_font_color,
                size=legend_font_size
            )
        )
    )

    # Display chart
    st.plotly_chart(fig)

#-----------------

def create_stacked_bar_chart(df, main_col_indices=[2, 4], main_row_index=0, main_colors=['#f54291', '#542ad1'],
                             sub_col_indices=None, sub_row_index=0, sub_colors=['#f54291', '#542ad1'],
                             legend_font_color='#000000', legend_font_size=12, text_color='#000000', text_font_size=14,
                             x_axis_label=None):
    
    # Get data for the main Stacked Bar Chart
    main_labels = df.columns[main_col_indices[0]:main_col_indices[-1] + 1]
    main_data = df.iloc[main_row_index, main_col_indices[0]:main_col_indices[-1] + 1]
    main_colors = main_colors
    
    # Create traces for the main Stacked Bar Chart
    main_trace = go.Bar(
        x=main_labels,
        y=main_data,
        marker=dict(color=main_colors),
        name='Main Category'
    )

    # Check if sub_col_indices is provided
    if sub_col_indices is not None:
        # Get data for the breakdown of the main category
        sub_labels = df.columns[sub_col_indices[0]:sub_col_indices[-1] + 1]
        sub_data = df.iloc[sub_row_index, sub_col_indices[0]:sub_col_indices[-1] + 1]
        sub_colors = sub_colors

        # Create traces for the breakdown of the main category
        sub_trace = go.Bar(
            x=sub_labels,
            y=sub_data,
            marker=dict(color=sub_colors),
            name='Subcategories'
        )
        
        # Add both main and sub traces to data
        data = [main_trace, sub_trace]
    else:
        # If sub_col_indices is not provided, only use the main trace
        data = [main_trace]

    # Create the layout
    layout = go.Layout(
        barmode='stack',
        title='Stacked Bar Chart with Original Numbers Breakdown',
        xaxis=dict(title='Category'),
        yaxis=dict(title='Count'),
        showlegend=True
    )

    # Update x-axis label if provided
    if x_axis_label:
        layout.xaxis.title = x_axis_label
    
    # Create the figure
    fig = go.Figure(data=data, layout=layout)
    
    # Show the figure using Plotly's Streamlit function
    st.plotly_chart(fig)


# ------------------------------
# Load the selected dataframe
df_path = os.path.join(dir, selected_df_name)
df = pd.read_csv(df_path)

# ------------------------- Table

# Create a custom table
fig = create_custom_table(df, 
                          header_fill_color='#0F123D', header_font_color='#F4BA41', header_font_size=11, header_alignment= 'center', header_line_color='#118DFF', header_line_width=.75,
                          cell_fill_color='#0F123D', cell_font_color='#04CEDC', cell_font_size=10, cell_alignment= 'center', cell_line_color='#118DFF', cell_line_width=.25)

# Write the name of the selected dataframe
st.write(f"Table: {selected_df_name}:")

# Display the table in Streamlit
st.plotly_chart(fig)


# -----------------------
# Get selected dataframe
#selected_df_path = os.path.join(dir, selected_df_name)
#df = pd.read_csv(selected_df_path)

# Check the filename and call the appropriate function
if selected_df_name == 'Types_of_Functional_Locations.csv':
    create_stacked_bar_chart(df,
                             main_col_indices=[2, 3],
                             main_row_index=0,
                             main_colors=['#f54291', '#542ad1'],
                             legend_font_color='#000000',
                             legend_font_size=12,
                             text_color='#000000',
                             text_font_size=14,
                             x_axis_label=selected_df_name)
    plot_donut_chart(df, 
                     col_indices=[4, 6], 
                     row_index=0, 
                     colors=['#ff0000', '#00ff00'], 
                     legend_font_color='#0000ff', 
                     legend_font_size=14,
                     text_color='#0000ff', 
                     text_font_size=14, 
                     textinfo='label+percent', 
                     textposition='outside',
                     marker=dict(colors=['#ff0000', '#00ff00'], line=dict(color='#000000', width=2)),
                     pull=[0, 0.03],
                     rotation=180,
                     hole=0.6)

elif selected_df_name == 'Non-PU_MU_Object_Type_Analysis.csv':
    new_df = df.iloc[:, [1, 4]]
    create_stacked_bar_chart(new_df,
                             main_col_indices=[0, 1],
                             main_row_index=0,
                             main_colors=['#f54291', '#542ad1'],
                             legend_font_color='#000000',
                             legend_font_size=12,
                             text_color='#000000',
                             text_font_size=14,
                             x_axis_label=selected_df_name)
    plot_donut_chart(df, 
                     col_indices=[2, 3], 
                     row_index=0, 
                     colors=['#ff0000', '#00ff00'], 
                     legend_font_color='#0000ff', 
                     legend_font_size=14,
                     text_color='#0000ff', 
                     text_font_size=14, 
                     textinfo='label+percent', 
                     textposition='outside',
                     marker=dict(colors=['#ff0000', '#00ff00'], line=dict(color='#000000', width=2)),
                     pull=[0, 0.03],
                     rotation=180,
                     hole=0.6)

elif selected_df_name == 'MU_Catg_Prof_Chks.csv':
    create_stacked_bar_chart(df,
                             main_col_indices=[1, 3],
                             main_row_index=0,
                             main_colors=['#f54291', '#542ad1'],
                             legend_font_color='#000000',
                             legend_font_size=12,
                             text_color='#000000',
                             text_font_size=14,
                             x_axis_label=selected_df_name)

elif selected_df_name == 'PU_Object_Type_Analysis.csv':
    plot_donut_chart(df, 
                     col_indices=[1, 3], 
                     row_index=0, 
                     colors=['#ff0000', '#00ff00'], 
                     legend_font_color='#0000ff', 
                     legend_font_size=14,
                     text_color='#0000ff', 
                     text_font_size=14, 
                     textinfo='label+percent', 
                     textposition='outside',
                     marker=dict(colors=['#ff0000', '#00ff00'], line=dict(color='#000000', width=2)),
                     pull=[0, 0.03],
                     rotation=180,
                     hole=0.6)

elif selected_df_name == 'PU_Child_Structure_Check.csv':
    plot_donut_chart(df, 
                     col_indices=[1, 2], 
                     row_index=0, 
                     colors=['#ff0000', '#00ff00'], 
                     legend_font_color='#0000ff', 
                     legend_font_size=14,
                     text_color='#0000ff', 
                     text_font_size=14, 
                     textinfo='label+percent', 
                     textposition='outside',
                     marker=dict(colors=['#ff0000', '#00ff00'], line=dict(color='#000000', width=2)),
                     pull=[0, 0.03],
                     rotation=180,
                     hole=0.6)
    plot_donut_chart(df,
                     col_indices=[3, 4], 
                     row_index=0, 
                     colors=['#ff0000', '#00ff00'], 
                     legend_font_color='#0000ff', 
                     legend_font_size=14,
                     text_color='#0000ff', 
                     text_font_size=14, 
                     textinfo='label+percent', 
                     textposition='outside',
                     marker=dict(colors=['#ff0000', '#00ff00'], line=dict(color='#000000', width=2)),
                     pull=[0, 0.03],
                     rotation=180,
                     hole=0.6)

elif selected_df_name == 'PU_CT_Check.csv':
    plot_donut_chart(df,
                     col_indices=[1, 2], 
                     row_index=0, 
                     colors=['#ff0000', '#00ff00'], 
                     legend_font_color='#0000ff', 
                     legend_font_size=14,
                     text_color='#0000ff', 
                     text_font_size=14, 
                     textinfo='label+percent', 
                     textposition='outside',
                     marker=dict(colors=['#ff0000', '#00ff00'], line=dict(color='#000000', width=2)),
                     pull=[0, 0.03],
                     rotation=180,
                     hole=0.6)
elif selected_df_name == 'Non-PU_MU_CT_&_Model_Analysis.csv':
    plot_donut_chart(df,
                     col_indices=[1, 4], 
                     row_index=0, 
                     colors=['#ff0000', '#00ff00'], 
                     legend_font_color='#0000ff', 
                     legend_font_size=14,
                     text_color='#0000ff', 
                     text_font_size=14, 
                     textinfo='label+percent', 
                     textposition='outside',
                     marker=dict(colors=['#ff0000', '#00ff00'], line=dict(color='#000000', width=2)),
                     pull=[0, 0.03],
                     rotation=180,
                     hole=0.6)
elif selected_df_name == 'PU_CT_&_Model_Analysis.csv':
    plot_donut_chart(df,
                     col_indices=[1, 4], 
                     row_index=0, 
                     colors=['#ff0000', '#00ff00'], 
                     legend_font_color='#0000ff', 
                     legend_font_size=14,
                     text_color='#0000ff', 
                     text_font_size=14, 
                     textinfo='label+percent', 
                     textposition='outside',
                     marker=dict(colors=['#ff0000', '#00ff00'], line=dict(color='#000000', width=2)),
                     pull=[0, 0.03],
                     rotation=180,
                     hole=0.6)
elif selected_df_name == 'FL_Catg_N__NAVI__UsrSt_Checks.csv':
    create_stacked_bar_chart(df,
                             main_col_indices=[1, 2],
                             main_row_index=0,
                             main_colors=['#f54291', '#542ad1'],
                             legend_font_color='#000000',
                             legend_font_size=12,
                             text_color='#000000',
                             text_font_size=14,
                             x_axis_label=selected_df_name)
    plot_donut_chart(df,
                     col_indices=[3, 4], 
                     row_index=0, 
                     colors=['#ff0000', '#00ff00'], 
                     legend_font_color='#0000ff', 
                     legend_font_size=14,
                     text_color='#0000ff', 
                     text_font_size=14, 
                     textinfo='label+percent', 
                     textposition='outside',
                     marker=dict(colors=['#ff0000', '#00ff00'], line=dict(color='#000000', width=2)),
                     pull=[0, 0.03],
                     rotation=180,
                     hole=0.6)

elif selected_df_name == 'Misc.csv':
    Misc_selection= st.selectbox('Pick a figure', ('Misc' , 'PU_Child_PG_and_WC_Data_Orig_Chks'))
    # Load the selected dataframe
    if Misc_selection == 'Misc':
        create_stacked_bar_chart(df,
                                 main_col_indices=[1, 1],
                                 main_row_index=0,
                                 main_colors=['#f54291', '#542ad1'],
                                 legend_font_color='#000000',
                                 legend_font_size=12,
                                 text_color='#000000',
                                 text_font_size=14,
                                 x_axis_label=selected_df_name)
    elif Misc_selection == 'PU_Child_PG_and_WC_Data_Orig_Chks':
        #t_path = os.path.join(dir, 'PU_Child_PG_and_WC_Data_Orig_Chks.csv')
        #t_df = pd.read_csv(t_path)
        t_df = pd.read_csv('./Data_Streamlit/PU_Child_PG_and_WC_Data_Orig_Chks.csv')
        # Create a custom table
        tb = create_custom_table(t_df, 
                          header_fill_color='#0F123D', header_font_color='#F4BA41', header_font_size=11, header_alignment= 'center', header_line_color='#118DFF', header_line_width=.75,
                          cell_fill_color='#0F123D', cell_font_color='#04CEDC', cell_font_size=10, cell_alignment= 'center', cell_line_color='#118DFF', cell_line_width=.25)
        # Write the name of the selected dataframe
        st.write("Table: PU_Child_PG_and_WC_Data_Orig_Chks")
        # Display the table in Streamlit
        st.plotly_chart(tb)
        # Drawing figure
        create_stacked_bar_chart(t_df,
                                 main_col_indices=[1, 5],
                                 main_row_index=0,
                                 main_colors=['#f54291', '#542ad1'],
                                 legend_font_color='#000000',
                                 legend_font_size=12,
                                 text_color='#000000',
                                 text_font_size=14,
                                 x_axis_label='PU_Child_PG_and_WC_Data_Orig_Chks.csv')

elif selected_df_name == 'PU_Child_PG_and_WC_Data_Orig_Chks.csv':
    create_stacked_bar_chart(df,
                             main_col_indices=[1, 5],
                             main_row_index=0,
                             main_colors=['#f54291', '#542ad1'],
                             legend_font_color='#000000',
                             legend_font_size=12,
                             text_color='#000000',
                             text_font_size=14,
                             x_axis_label=selected_df_name)

elif selected_df_name == 'PU_Child_UsrSt__Asset_Under_Const___AUCN__Chks.csv':
    create_stacked_bar_chart(df,
                             main_col_indices=[1, 4],
                             main_row_index=0,
                             main_colors=['#f54291', '#542ad1'],
                             legend_font_color='#000000',
                             legend_font_size=12,
                             text_color='#000000',
                             text_font_size=14,
                             x_axis_label=selected_df_name)
    

elif selected_df_name == 'PU_Child_System_Status_Comparisons.csv':
    create_stacked_bar_chart(df,
                             main_col_indices=[1, 4],
                             main_row_index=0,
                             main_colors=['#f54291', '#542ad1'],
                             legend_font_color='#000000',
                             legend_font_size=12,
                             text_color='#000000',
                             text_font_size=14,
                             x_axis_label=selected_df_name)

elif selected_df_name == 'Plnr_Group_Data_Origin_Checks.csv':
    create_stacked_bar_chart(df,
                             main_col_indices=[1, 2],
                             main_row_index=0,
                             main_colors=['#f54291', '#542ad1'],
                             legend_font_color='#000000',
                             legend_font_size=12,
                             text_color='#000000',
                             text_font_size=14,
                             x_axis_label=selected_df_name)
    
elif selected_df_name == 'PU_Child_UsrSt__Not_on_Site___Decom___SOLD_DCOM__Chks.csv':
    create_stacked_bar_chart(df,
                             main_col_indices=[1, 4],
                             main_row_index=0,
                             main_colors=['#f54291', '#542ad1'],
                             legend_font_color='#000000',
                             legend_font_size=12,
                             text_color='#000000',
                             text_font_size=14,
                             x_axis_label=selected_df_name)

elif selected_df_name == 'Usr_Stat_AUCN_SOLD_DCOM_and_Sys_S.csv':
    create_stacked_bar_chart(df,
                             main_col_indices=[1, 12],
                             main_row_index=0,
                             main_colors=['#f54291', '#542ad1'],
                             legend_font_color='#000000',
                             legend_font_size=12,
                             text_color='#000000',
                             text_font_size=14,
                             x_axis_label=selected_df_name)

elif selected_df_name == 'Work_Center_Data_Origin_Checks.csv':
    create_stacked_bar_chart(df,
                             main_col_indices=[1, 2],
                             main_row_index=0,
                             main_colors=['#f54291', '#542ad1'],
                             legend_font_color='#000000',
                             legend_font_size=12,
                             text_color='#000000',
                             text_font_size=14,
                             x_axis_label=selected_df_name)


