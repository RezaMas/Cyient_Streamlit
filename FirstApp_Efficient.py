# Web App with Streamlit

# Author: Reza Masoudian, Created on July 25, 2023
# ---------------------------------------------------------
import pandas as pd
import streamlit as st
#import numpy as np
import plotly.graph_objects as go
import os
print(os.getcwd())
# ----------------------------------------------------------
# -------------- Page layout and properties ----------------
# dashboard title

st.set_page_config(page_title='Visualisation of Data',
                   page_icon='Active', layout='wide')

st.image('./logo.png', use_column_width=True)
st.title('Sample Dashboard')

# -------------

# Dashboard Features
#st.sidebar.image('./logo_dashboard.png', use_column_width= True)

st.sidebar.header('Input Parameters')


# Directory where the dataframes are stored
dir = './Data_Streamlit_eff'

# Get a list of the dataframe names
df_names = os.listdir(dir)

# Remove any non .csv files if present
df_names = [df for df in df_names if df.endswith('.csv')]

# Sidebar selectbox for dataframe selection
selected_df_name = st.sidebar.selectbox('Select a dataframe', df_names)

# --------------------------------------------------------------------

#--------- Tables
# Table function

# It's writtem im the compact form of create_stacked_bar_chart
def create_custom_table(df,
                          header_fill_color='#34495E', header_font_color='#FFFF00', header_font_size=10, header_alignment='center', header_line_color='#34495E', header_line_width=.75,
                          cell_fill_color='#34495E', cell_font_color='#FFFFFF', cell_font_size=10, cell_alignment='center', cell_line_color='#34495E', cell_line_width=.25):

    # Convert the dataframe to a list of lists
    df_values = [df[col].tolist() for col in df.columns]

    # Create a table
    fig = go.Figure(data=[go.Table(
        header=dict(values=df.columns.tolist(),
                    fill_color=header_fill_color,
                    align=header_alignment,
                    line=dict(color=header_line_color,
                              width=header_line_width),
                    font=dict(color=header_font_color, size=header_font_size)),
        cells=dict(values=df_values,
                   fill_color=cell_fill_color,
                   align=cell_alignment,
                   line=dict(color=cell_line_color, width=cell_line_width),
                   font=dict(color=cell_font_color, size=cell_font_size)))
    ])

    return fig

#-------- Diagrams
# ------------------------

# It's writtem im the compact form of create_stacked_bar_chart
def plot_donut_chart(df, col_indices=[1, 5], row_index=0, legend_font_color='#30587e', legend_font_size=11, text_color='#30587e', text_font_size=11,
                     textinfo='label+percent', textposition='outside', marker=dict(colors=['#4F81BD', '#8DA0CB', '#66C2A5', '#E78AC3', '#FC8D62'], line=dict(color='#000000', width=2)),
                     pull=[0.1, 0.1], rotation=90, hole=0.6):
    
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

# -----------------
# ina nemitoonan ba ham bashan: bar_width=0.2, bargap=.05
# baraye rang legend ina bayad documentation plotly ro check konam.


def create_stacked_bar_chart(df, main_col_indices=[2, 4], main_row_index=0, main_colors=['#48bdbb', '#4884bd', '#8DA0CB', '#E78AC3', '#E1E055', '#D755D5'],
                             sub_col_indices=None, sub_row_index=0, sub_colors=['#f54291', '#542ad1'],
                             legend_font_color='#000000', legend_font_size=11, text_color='#000000', text_font_size=11,
                             x_axis_label=None, bar_width=0.2, bargap=.05, figure_width=400, figure_height=400):

    # Get data for the main Stacked Bar Chart
    main_labels = df.columns[main_col_indices[0]:main_col_indices[-1] + 1]
    main_data = df.iloc[main_row_index,
                        main_col_indices[0]:main_col_indices[-1] + 1]
    main_colors = main_colors

    # Create traces for the main Stacked Bar Chart
    main_trace = go.Bar(
        x=main_labels,
        y=main_data,
        width=bar_width,
        marker=dict(color=main_colors),
        name='Main Category'
    )

    # Check if sub_col_indices is provided
    if sub_col_indices is not None:
        # Get data for the breakdown of the main category
        sub_labels = df.columns[sub_col_indices[0]:sub_col_indices[-1] + 1]
        sub_data = df.iloc[sub_row_index,
                           sub_col_indices[0]:sub_col_indices[-1] + 1]
        sub_colors = sub_colors

        # Create traces for the breakdown of the main category
        sub_trace = go.Bar(
            x=sub_labels,
            y=sub_data,
            width=bar_width,
            marker=dict(color=sub_colors),
            name=None #'Subcategories'
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
        bargap=bargap,
        width=figure_width,
        height=figure_height,
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

col1, col2 = st.columns(2)
with col1:
    # Create a custom table
    # Write the name of the selected dataframe
    st.write(f"Table: {selected_df_name}:")
    fig = create_custom_table(df,
                              header_fill_color='#34495E', header_font_color='#FFFF00', header_font_size=10, header_alignment='center', header_line_color='#34495E', header_line_width=.75,
                              cell_fill_color='#34495E', cell_font_color='#FFFFFF', cell_font_size=10, cell_alignment='center', cell_line_color='#34495E', cell_line_width=.25)

    # Display the table in Streamlit
    st.plotly_chart(fig)
    with st.expander("See Explanation"):
        st.write(
            'We will put the description of tables, here! (if loop would be needed)')

# ----------------------- Figures
# Get selected dataframe
#selected_df_path = os.path.join(dir, selected_df_name)
#df = pd.read_csv(selected_df_path)

# Check the filename and call the appropriate function
with col2:
    if selected_df_name == 'Types_of_Functional_Locations.csv':
        create_stacked_bar_chart(df,
                                 main_col_indices=[2, 3],
                                 main_row_index=0,
                                 main_colors=['#48bdbb', '#4884bd'],
                                 legend_font_color='#406060',
                                 legend_font_size=11,
                                 text_color='#406060',
                                 text_font_size=11,
                                 x_axis_label=selected_df_name,
                                 bar_width=0.2,
                                 bargap=.1,
                                 figure_width=400,
                                 figure_height=400)
        plot_donut_chart(df,
                         col_indices=[4, 5],
                         row_index=0,
                         legend_font_color='#30587e',
                         legend_font_size=11,
                         text_color='#30587e',
                         text_font_size=11,
                         textinfo='label+percent',
                         textposition='outside',
                         marker=dict(colors=['#28455b', '#748c94'], line=None),
                         pull=[0, 0.03],
                         rotation=180,
                         hole=0.6)
        with st.expander("See Explanation"):
            st.write('We will put the description of figures, here!')

    elif selected_df_name == 'Non-PU_MU_Object_Type_Analysis.csv':
        new_df = df.iloc[:, [1, 4]]
        create_stacked_bar_chart(new_df,
                                 main_col_indices=[0, 1],
                                 main_row_index=0,
                                 main_colors=['#48bdbb', '#4884bd'],
                                 legend_font_color='#406060',
                                 legend_font_size=11,
                                 text_color='#406060',
                                 text_font_size=11,
                                 x_axis_label=selected_df_name,
                                 bar_width=0.2,
                                 bargap=.1,
                                 figure_width=400,
                                 figure_height=400)
        plot_donut_chart(df,
                         col_indices=[2, 3],
                         row_index=0,
                         legend_font_color='#30587e',
                         legend_font_size=11,
                         text_color='#30587e',
                         text_font_size=11,
                         textinfo='label+percent',
                         textposition='outside',
                         marker=dict(colors=['#28455b', '#748c94'], line=None),
                         pull=[0, 0.03],
                         rotation=60,
                         hole=0.6)
        with st.expander("See Explanation"):
            st.write('We will put the description of figures, here!')

    elif selected_df_name == 'MU_Catg_Prof_Chks.csv':
        create_stacked_bar_chart(df,
                                 main_col_indices=[1, 3],
                                 main_row_index=0,
                                 main_colors=['#48bdbb', '#4884bd', '#728c69'],
                                 legend_font_color='#406060',
                                 legend_font_size=11,
                                 text_color='#406060',
                                 text_font_size=11,
                                 x_axis_label=selected_df_name,
                                 bar_width=0.2,
                                 bargap=.1,
                                 figure_width=400,
                                 figure_height=400)
        with st.expander("See Explanation"):
            st.write('We will put the description of figures, here!')

    elif selected_df_name == 'PU_Object_Type_Analysis.csv':
        plot_donut_chart(df,
                         col_indices=[1, 3],
                         row_index=0,
                         legend_font_color='#30587e',
                         legend_font_size=11,
                         text_color='#30587e',
                         text_font_size=11,
                         textinfo='label+percent',
                         textposition='outside',
                         marker=dict(colors=['#4F81BD', '#8DA0CB', '#66C2A5'], line=None),
                         pull=[0, 0.03],
                         rotation=180,
                         hole=0.6)
        with st.expander("See Explanation"):
            st.write('We will put the description of figures, here!')

    elif selected_df_name == 'PU_Child_Structure_Check.csv':
        plot_donut_chart(df,
                         col_indices=[1, 2],
                         row_index=0,
                         legend_font_color='#30587e',
                         legend_font_size=11,
                         text_color='#30587e',
                         text_font_size=11,
                         textinfo='label+percent',
                         textposition='outside',
                         marker=dict(colors=['#48bdbb', '#4884bd'], line=None),
                         pull=[0, 0.03],
                         rotation=180,
                         hole=0.6)
        plot_donut_chart(df,
                         col_indices=[3, 4],
                         row_index=0,
                         legend_font_color='#30587e',
                         legend_font_size=11,
                         text_color='#30587e',
                         text_font_size=11,
                         textinfo='label+percent',
                         textposition='outside',
                         marker=dict(colors=['#28455b', '#748c94'], line=None),
                         pull=[0, 0.03],
                         rotation=180,
                         hole=0.6)
        with st.expander("See Explanation"):
            st.write('We will put the description of figures, here!')

    elif selected_df_name == 'PU_CT_Check.csv':
        plot_donut_chart(df,
                         col_indices=[1, 2],
                         row_index=0,
                         legend_font_color='#30587e',
                         legend_font_size=11,
                         text_color='#30587e',
                         text_font_size=11,
                         textinfo='label+percent',
                         textposition='outside',
                         marker=dict(colors=['#48bdbb', '#4884bd'], line=None),
                         pull=[0, 0.03],
                         rotation=180,
                         hole=0.6)
        with st.expander("See Explanation"):
            st.write('We will put the description of figures, here!')

    elif selected_df_name == 'Non-PU_MU_CT_&_Model_Analysis.csv':
        plot_donut_chart(df,
                         col_indices=[1, 4],
                         row_index=0,
                         legend_font_color='#30587e',
                         legend_font_size=11,
                         text_color='#30587e',
                         text_font_size=11,
                         textinfo='label+percent',
                         textposition='outside',
                         marker=dict(colors=['#48bdbb', '#4884bd', '#28455b', '#748c94'], line=None),
                         pull=[0, 0.03],
                         rotation=180,
                         hole=0.6)
        with st.expander("See Explanation"):
            st.write('We will put the description of figures, here!')

    elif selected_df_name == 'PU_CT_&_Model_Analysis.csv':
        plot_donut_chart(df,
                         col_indices=[1, 4],
                         row_index=0,
                         legend_font_color='#30587e',
                         legend_font_size=11,
                         text_color='#30587e',
                         text_font_size=11,
                         textinfo='label+percent',
                         textposition='outside',
                         marker=dict(colors=['#48bdbb', '#4884bd', '#28455b', '#748c94'], line=None),
                         pull=[0, 0.03],
                         rotation=180,
                         hole=0.6)
        with st.expander("See Explanation"):
            st.write('We will put the description of figures, here!')

    elif selected_df_name == 'FL_Catg_N__NAVI__UsrSt_Checks.csv':
        create_stacked_bar_chart(df,
                                 main_col_indices=[1, 2],
                                 main_row_index=0,
                                 main_colors=['#48bdbb', '#4884bd'],
                                 legend_font_color='#406060',
                                 legend_font_size=11,
                                 text_color='#406060',
                                 text_font_size=11,
                                 x_axis_label=selected_df_name,
                                 bar_width=0.2,
                                 bargap=.1,
                                 figure_width=400,
                                 figure_height=400)
        plot_donut_chart(df,
                         col_indices=[3, 4],
                         row_index=0,
                         legend_font_color='#30587e',
                         legend_font_size=11,
                         text_color='#30587e',
                         text_font_size=11,
                         textinfo='label+percent',
                         textposition='outside',
                         marker=dict(colors=['#28455b', '#748c94'], line=None),
                         pull=[0, 0.03],
                         rotation=180,
                         hole=0.6)
        with st.expander("See Explanation"):
            st.write('We will put the description of figures, here!')

    elif selected_df_name == 'Misc.csv':
        Misc_selection = st.selectbox(
            'Pick a figure', ('Misc', 'PU_Child_PG_and_WC_Data_Orig_Chks'))
        # Load the selected dataframe
        if Misc_selection == 'Misc':
            create_stacked_bar_chart(df,
                                     main_col_indices=[1, 1],
                                     main_row_index=0,
                                     main_colors=['#48bdbb'],
                                     legend_font_color='#406060',
                                     legend_font_size=11,
                                     text_color='#406060',
                                     text_font_size=11,
                                     x_axis_label=selected_df_name,
                                     bar_width=0.2,
                                     bargap=.1,
                                     figure_width=400,
                                     figure_height=400)
            with st.expander("See Explanation"):
                st.write('We will put the description of figures, here!')
        elif Misc_selection == 'PU_Child_PG_and_WC_Data_Orig_Chks':
            #t_path = os.path.join(dir, 'PU_Child_PG_and_WC_Data_Orig_Chks.csv')
            #t_df = pd.read_csv(t_path)
            t_df = pd.read_csv(
                './Data_Streamlit_eff/PU_Child_PG_and_WC_Data_Orig_Chks.csv')
            # Create a custom table
            with col1:
                tb = create_custom_table(t_df,
                                         header_fill_color='#34495E', header_font_color='#FFFF00', header_font_size=10, header_alignment='center', header_line_color='#34495E', header_line_width=.75,
                                         cell_fill_color='#34495E', cell_font_color='#FFFFFF', cell_font_size=10, cell_alignment='center', cell_line_color='#34495E', cell_line_width=.25)
                # Write the name of the selected dataframe
                st.write("Table: PU_Child_PG_and_WC_Data_Orig_Chks")
                # Display the table in Streamlit
                st.plotly_chart(tb)
                with st.expander("See Explanation"):
                    st.write('We will put the description of figures, here!')
            # Drawing figure
            create_stacked_bar_chart(t_df,
                                     main_col_indices=[1, 5],
                                     main_row_index=0,
                                     main_colors=['#48bdbb', '#4884bd', '#8DA0CB', '#F296C4', '#E78AC3'],
                                     legend_font_color='#406060',
                                     legend_font_size=11,
                                     text_color='#406060',
                                     text_font_size=11,
                                     x_axis_label=selected_df_name,
                                     bar_width=0.2,
                                     bargap=.1,
                                     figure_width=400,
                                     figure_height=400)
            with st.expander("See Explanation"):
                st.write('We will put the description of figures, here!')

    elif selected_df_name == 'PU_Child_PG_and_WC_Data_Orig_Chks.csv':
        create_stacked_bar_chart(df,
                                 main_col_indices=[1, 5],
                                 main_row_index=0,
                                 main_colors=['#48bdbb', '#4884bd', '#8DA0CB', '#E78AC3', '#E1E055'],
                                 legend_font_color='#406060',
                                 legend_font_size=11,
                                 text_color='#406060',
                                 text_font_size=11,
                                 x_axis_label=selected_df_name,
                                 bar_width=0.2,
                                 bargap=.1,
                                 figure_width=400,
                                 figure_height=400)
        with st.expander("See Explanation"):
            st.write('We will put the description of figures, here!')

    elif selected_df_name == 'PU_Child_UsrSt__Asset_Under_Const___AUCN__Chks.csv':
        create_stacked_bar_chart(df,
                                 main_col_indices=[1, 4],
                                 main_row_index=0,
                                 main_colors=['#48bdbb', '#4884bd', '#8DA0CB', '#E78AC3'],
                                 legend_font_color='#406060',
                                 legend_font_size=11,
                                 text_color='#406060',
                                 text_font_size=11,
                                 x_axis_label=selected_df_name,
                                 bar_width=0.2,
                                 bargap=.1,
                                 figure_width=400,
                                 figure_height=400)
        with st.expander("See Explanation"):
            st.write('We will put the description of figures, here!')

    elif selected_df_name == 'PU_Child_System_Status_Comparisons.csv':
        create_stacked_bar_chart(df,
                                 main_col_indices=[1, 4],
                                 main_row_index=0,
                                 main_colors=['#48bdbb', '#4884bd', '#8DA0CB', '#E78AC3'],
                                 legend_font_color='#406060',
                                 legend_font_size=11,
                                 text_color='#406060',
                                 text_font_size=11,
                                 x_axis_label=selected_df_name,
                                 bar_width=0.2,
                                 bargap=.1,
                                 figure_width=400,
                                 figure_height=400)
        with st.expander("See Explanation"):
            st.write('We will put the description of figures, here!')

    elif selected_df_name == 'Plnr_Group_Data_Origin_Checks.csv':
        create_stacked_bar_chart(df,
                                 main_col_indices=[1, 2],
                                 main_row_index=0,
                                 main_colors=['#48bdbb', '#4884bd'],
                                 legend_font_color='#406060',
                                 legend_font_size=11,
                                 text_color='#406060',
                                 text_font_size=11,
                                 x_axis_label=selected_df_name,
                                 bar_width=0.2,
                                 bargap=.1,
                                 figure_width=400,
                                 figure_height=400)
        with st.expander("See Explanation"):
            st.write('We will put the description of figures, here!')

    elif selected_df_name == 'PU_Child_UsrSt__Not_on_Site___Decom___SOLD_DCOM__Chks.csv':
        create_stacked_bar_chart(df,
                                 main_col_indices=[1, 4],
                                 main_row_index=0,
                                 main_colors=['#48bdbb', '#E78AC3', '#8DA0CB', '#4884bd'],
                                 legend_font_color='#406060',
                                 legend_font_size=11,
                                 text_color='#406060',
                                 text_font_size=11,
                                 x_axis_label=selected_df_name,
                                 bar_width=0.2,
                                 bargap=.1,
                                 figure_width=400,
                                 figure_height=400)
        with st.expander("See Explanation"):
            st.write('We will put the description of figures, here!')

    elif selected_df_name == 'Usr_Stat_AUCN_SOLD_DCOM_and_Sys_S.csv':
        create_stacked_bar_chart(df,
                                 main_col_indices=[1, 12],
                                 main_row_index=0,
                                 main_colors=['#48bdbb', '#4884bd', '#8DA0CB', '#E78AC3'],
                                 legend_font_color='#406060',
                                 legend_font_size=11,
                                 text_color='#406060',
                                 text_font_size=11,
                                 x_axis_label=selected_df_name,
                                 bar_width=0.2,
                                 bargap=.1,
                                 figure_width=400,
                                 figure_height=400)
        with st.expander("See Explanation"):
            st.write('We will put the description of figures, here!')

    elif selected_df_name == 'Work_Center_Data_Origin_Checks.csv':
        create_stacked_bar_chart(df,
                                 main_col_indices=[1, 2],
                                 main_row_index=0,
                                 main_colors=['#48bdbb', '#4884bd'],
                                 legend_font_color='#406060',
                                 legend_font_size=11,
                                 text_color='#406060',
                                 text_font_size=11,
                                 x_axis_label=selected_df_name,
                                 bar_width=0.2,
                                 bargap=.1,
                                 figure_width=400,
                                 figure_height=400)
        with st.expander("See Explanation"):
            st.write('We will put the description of figures, here!')
    
    elif selected_df_name == 'PU_Child_PG_and_WC_Data_Orig_Chks.csv':
        create_stacked_bar_chart(df,
                                 main_col_indices=[1, 5],
                                 main_row_index=0,
                                 main_colors=['#48bdbb', '#4884bd', '#8DA0CB', '#F296C4', '#E78AC3'],
                                 legend_font_color='#406060',
                                 legend_font_size=11,
                                 text_color='#406060',
                                 text_font_size=11,
                                 x_axis_label=selected_df_name,
                                 bar_width=0.2,
                                 bargap=.1,
                                 figure_width=400,
                                 figure_height=400)
        with st.expander("See Explanation"):
            st.write('We will put the description of figures, here!')


