# Image_Organizer

A python tool to organize and copy image files based on file type, mod time and containing directory.

While this tool is primarily intended to help organize image files (e.g., when dumping camera SD cards) it will accept a comma separated list of any file extensions and perform the same function.

## Usage:

```python3 Image_Organizer.py <Input Directory> <Output Director> <File Types>```

## Example:
```python3 Image_Organizer.py /Path/To/Input /Path/To/Output DNG,JPG```

Files and folders discovered in /Path/To/Input.
```
├── 100US100
│   ├── L1000001.DNG
│   ├── L1000001.JPG
│   ├── L1000002.DNG
│   ├── L1000002.JPG
├── 100US101
│   ├── L1000003.DNG
│   ├── L1000004.DNG
│   └── L1000005.DNG
└── 100US102
    ├── L1000006.DNG
    ├── L1000007.DNG
    ├── L1000008.DNG
```

New folder structure created in /Path/To/Output. Files are copied to appropriate path based on containing folder, file type and mod time.
```
├── 100US100
│   ├── DNG
│   │   ├── 2026-01-31
│   │   │   ├── L1000001.DNG
│   │   │   ├── L1000002.DNG
│   └── JPG
│       └── 2026-01-31
│           ├── L1000001.JPG
│           ├── L1000002.JPG
├── 100US101
│   └── DNG
│       └── 2026-02-01
│           ├── L1000003.DNG
│           ├── L1000004.DNG
│           └── L1000005.DNG
└── 100US102
    └── DNG
        ├── 2026-03-01
        │   └── L1000006.DNG
        ├── 2026-03-02
        │   └── L1000007.DNG
        ├── 2026-03-03
        │   └── L1000008.DNG
```
