# Wrapper for the fastest file/folder list tool (UFFS) 350 GB in less than 3 Minutes (1.800.000 files and folders)

This module uses https://github.com/githubrobbi/Ultra-Fast-File-Search to list the files on your hard disk.
If the app is not installed, the function will try to install it. If you want to install it by yourself, 
DOWNLOAD THE .com FILE INSTEAD OF THE .exe FILE!

### Tested against Windows 10 / Python 3.10 / Anaconda 


## pip install uffspd


```python
# As you can see, there are only a few parameters that you can pass, 
but don't worry. The Fine-Grained filtering can be done easily with 
DataFrames


from uffspd import list_all_files
df1 = list_all_files(
    path2search="C:\\",
    file_extensions=None,
    uffs_com_path=r"C:\ProgramData\anaconda3\envs\adda\uffs.com",
)

df2 = list_all_files(
    path2search="c:\\Windows",
    file_extensions=[".log", ".txt", ".tmp"],
    uffs_com_path=r"C:\ProgramData\anaconda3\envs\adda\uffs.com",
)


df3 = list_all_files(
    path2search="c:\\Windows",
    file_extensions=None,
    uffs_com_path=None,
)


                                                                    aa_path                                                   aa_name             aa_path_only  aa_size  aa_size_on_disk              aa_created         aa_last_written        aa_last_accessed  aa_descendents  aa_read_only  aa_archive  aa_system  aa_hidden  aa_offline  aa_not_content_indexed_file  aa_no_scrub_file  aa_integrity  aa_pinned  aa_unpinned  aa_directory_flag  aa_compressed  aa_encrypted  aa_sparse  aa_reparse  aa_attributes
0                                                   C:\Windows\setuperr.log                                              setuperr.log               C:\Windows        0                0  b'2023-03-25 16:19:25'  b'2023-03-25 16:19:25'  b'2023-03-25 16:19:25'               0             0           1          0          0           0                            0                 0             0          0            0                  0              0             0          0           0             32
1                                               C:\Windows\TEMP\GeoInfo.tmp                                               GeoInfo.tmp          C:\Windows\TEMP        0                0  b'2023-03-25 07:32:24'  b'2023-04-02 09:28:45'  b'2023-04-02 09:28:45'               0             0           1          0          0           0                            0                 0             0          0            0                  0              0             0          0           0             32
2                    C:\Windows\TEMP\assistant_installer_20230325061854.log                    assistant_installer_20230325061854.log          C:\Windows\TEMP      345                0  b'2023-03-25 06:18:54'  b'2023-03-25 06:18:54'  b'2023-03-25 06:18:54'               0             0           1          0          0           0                            0                 0             0          0            0                  0              0             0          0           0             32
3                    C:\Windows\TEMP\assistant_installer_20230325061138.log                    assistant_installer_20230325061138.log          C:\Windows\TEMP      345                0  b'2023-03-25 06:11:38'  b'2023-03-25 06:11:38'  b'2023-03-25 06:11:38'               0             0           1          0          0           0                            0                 0             0          0            0                  0              0             0          0           0             32
4  C:\Windows\TEMP\AppxErrorReport_A796FED9-5EE8-0001-9753-97A7E85ED901.txt  AppxErrorReport_A796FED9-5EE8-0001-9753-97A7E85ED901.txt          C:\Windows\TEMP      688             4096  b'2023-03-25 05:43:05'  b'2023-03-25 05:43:05'  b'2023-03-25 05:43:05'               0             0           1          0          0           0                            0                 0             0          0            0                  0              0             0          0           0             32
5                                          C:\Windows\TEMP\HamachiSetup.log                                          HamachiSetup.log          C:\Windows\TEMP     4584             8192  b'2023-03-25 05:38:58'  b'2023-03-25 06:22:25'  b'2023-03-25 06:22:25'               0             0           1          0          0           0                            0                 0             0          0            0                  0              0             0          0           0             32
6                                    C:\Windows\TEMP\FXSAPIDebugLogFile.txt                                    FXSAPIDebugLogFile.txt          C:\Windows\TEMP        0                0  b'2023-03-25 13:11:40'  b'2023-03-25 13:11:40'  b'2023-03-25 13:11:40'               0             0           1          0          0           0                            0                 0             0          0            0                  0              0             0          0           0             32
7                                   C:\Windows\TEMP\FXSTIFFDebugLogFile.txt                                   FXSTIFFDebugLogFile.txt          C:\Windows\TEMP        0                0  b'2023-03-25 13:11:40'  b'2023-03-25 13:11:40'  b'2023-03-25 13:11:40'               0             0           1          0          0           0                            0                 0             0          0            0                  0              0             0          0           0             32
8                                 C:\Windows\TEMP\_avast_\nsfsp00000001.tmp                                         nsfsp00000001.tmp  C:\Windows\TEMP\_avast_        0                0  b'2023-04-07 03:03:50'  b'2023-04-07 15:16:59'  b'2023-04-07 15:16:59'               0             0           1          0          0           0                            0                 0             0          0            0                  0              0             0          0           0             32
9                                 C:\Windows\TEMP\_avast_\nsfsp00000003.tmp                                         nsfsp00000003.tmp  C:\Windows\TEMP\_avast_        0                0  b'2023-04-07 06:05:19'  b'2023-04-07 12:18:21'  b'2023-04-07 12:18:21'               0             0           1          0          0           0                            0                 0             0          0            0                  0              0             0          0           0             32
```