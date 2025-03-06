# import streamlit as st
# import pandas as pd
# import os
# from io import BytesIO

# st.set_page_config(page_title='Growth Mindset', layout='wide')

# # Custom CSS
# st.markdown(
#     """
#     <style>
#     .stApp {
#         background-color: #f5f5f5;
#         color: #000000;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # Title & Description
# st.title('Data Sweeper Sterling Integrator by Asma')
# st.write('Transform your files between CSV and Excel formats with built-in data cleaning tools.')

# # File uploader
# uploaded_files = st.file_uploader(
#     'Upload your input file (CSV and Excel formats accepted)', 
#     type=['csv', 'xlsx'], 
#     accept_multiple_files=True
# )

# if uploaded_files:
#     for file in uploaded_files:
#         file_extension = os.path.splitext(file.name)[-1].lower()

#         if file_extension == '.csv':
#             df = pd.read_csv(file)
#         elif file_extension == '.xlsx':
#             df = pd.read_excel(file)
#         else:
#             st.error(f'File format not supported: {file_extension}')
#             continue

#         # File Details
#         st.subheader(f'Preview of {file.name}')
#         st.dataframe(df.head())

#         # Data Cleaning Options
#         st.subheader(f'Data Cleaning Options for {file.name}')
#         if st.checkbox(f'Clean data for {file.name}'):
#             col1, col2 = st.columns(2)

#             with col1:
#                 if st.button(f"Remove duplicates from {file.name}"):
#                     df.drop_duplicates(inplace=True)
#                     st.write(f'Duplicates removed from {file.name}!')

#             with col2:
#                 if st.button(f"Fill missing values in {file.name}"):
#                     numeric_cols = df.select_dtypes(include=['number']).columns
#                     df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
#                     st.write(f'Missing values filled in {file.name}!')

#         # Select Columns
#         st.subheader(f"Select Columns to Keep for {file.name}")
#         columns = st.multiselect(f'Choose columns for {file.name}', df.columns, default=df.columns)
#         df = df[columns]

#         # Data Visualization
#         st.subheader(f"Data Visualization for {file.name}")
#         if st.checkbox(f"Show visualization for {file.name}"):
#             if df.select_dtypes(include='number').shape[1] >= 2:
#                 st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])
#             else:
#                 st.warning("Not enough numerical columns to display a chart.")

#         # Conversion Options
#         st.subheader(f"Conversion Options for {file.name}")
#         conversion_type = st.radio(f"Convert {file.name} to:", ['CSV', 'Excel'], key=file.name)

#         if st.button(f"Convert {file.name} to {conversion_type}"):
#             buffer = BytesIO()
#             if conversion_type == 'CSV':
#                 df.to_csv(buffer, index=False)
#                 file_name = file.name.replace(file_extension, '.csv')
#                 mime_type = 'text/csv'
#             else:  # Convert to Excel
#                 with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
#                     df.to_excel(writer, index=False)
#                 file_name = file.name.replace(file_extension, '.xlsx')
#                 mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

#             buffer.seek(0)
#             st.download_button(
#                 label=f"Download {file.name} as {conversion_type}",
#                 data=buffer,
#                 file_name=file_name,
#                 mime=mime_type
#             )

# # st.success("All files processed successfully!")

# if uploaded_files:
#     st.success("All files processed successfully!")
# else:
#     st.info("Please upload your file to get started.")


import streamlit as st
import pandas as pd
import os
import numpy as np
from io import BytesIO
from scipy.stats import zscore

st.set_page_config(page_title='Advanced Data Sweeper', layout='wide')

# Custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5f5f5;
        color: #000000;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title & Description
st.title('Advanced Data Sweeper - AI-Powered Data Processing')
st.write('Upload, clean, merge, analyze, and convert your CSV/Excel files seamlessly!')

# File uploader
uploaded_files = st.file_uploader(
    'Upload your files (CSV/Excel)', 
    type=['csv', 'xlsx'], 
    accept_multiple_files=True
)

def read_file(file):
    ext = os.path.splitext(file.name)[-1].lower()
    if ext == '.csv':
        return pd.read_csv(file), ext
    elif ext == '.xlsx':
        return pd.read_excel(file), ext
    else:
        return None, None

if uploaded_files:
    dataframes = {}
    for file in uploaded_files:
        df, ext = read_file(file)
        if df is not None:
            dataframes[file.name] = df
            st.subheader(f'Preview of {file.name}')
            st.dataframe(df.head())

    # Multi-File Merging
    if len(dataframes) > 1:
        st.subheader('Merge Files')
        common_columns = list(set.intersection(*[set(df.columns) for df in dataframes.values()]))
        if common_columns:
            merge_column = st.selectbox('Select column to merge on', common_columns)
            merge_type = st.selectbox('Merge type', ['inner', 'outer', 'left', 'right'])
            merged_df = pd.concat(dataframes.values(), join=merge_type, keys=dataframes.keys(), axis=0).reset_index(drop=True)
            st.write('Merged Data Preview:')
            st.dataframe(merged_df.head())
        else:
            st.warning('No common columns found for merging!')
    
    # AI-Powered Data Insights
    for file_name, df in dataframes.items():
        st.subheader(f'AI Insights for {file_name}')
        if st.checkbox(f'Show statistics for {file_name}'):
            st.write(df.describe())
        
        if st.checkbox(f'Detect anomalies in {file_name}'):
            num_cols = df.select_dtypes(include=['number']).columns
            for col in num_cols:
                df[f'{col}_zscore'] = zscore(df[col])
            st.write('Z-Score Calculated (values above 3 or below -3 are potential outliers)')
            st.dataframe(df[[col for col in df.columns if 'zscore' in col]].head())
    
    # Conversion & Download
    for file_name, df in dataframes.items():
        st.subheader(f'Convert {file_name}')
        conversion_type = st.radio(f'Convert {file_name} to:', ['CSV', 'Excel'], key=file_name)
        if st.button(f'Download {file_name} as {conversion_type}'):
            buffer = BytesIO()
            if conversion_type == 'CSV':
                df.to_csv(buffer, index=False)
                file_ext = '.csv'
                mime = 'text/csv'
            else:
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False)
                file_ext = '.xlsx'
                mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            buffer.seek(0)
            st.download_button(
                label=f'Download {file_name} as {conversion_type}',
                data=buffer,
                file_name=file_name.replace(os.path.splitext(file_name)[-1], file_ext),
                mime=mime
            )
else:
    st.info('Please upload your files to get started!')
