<p align="center">
<img src="https://github.com/timminator/Spatial-Media-Metadata-Injector/blob/master/spatialmedia/Spatial%20Media%20Metadata%20Injector.png" alt="Spatial Media Metadata Injector Icon" width="128">
  <h1 align="center">Spatial Media Metadata Injector</h1>
  </p>
</p>

<br>

## ℹ About

This repo provides an updated binary release with a few more bug fixes in comparison to the upstream repository for Windows and Linux. Binaries for the CLI version are also provided.

# Spatial Media Metadata Injector

A tool for manipulating spatial media 
([spherical video](../docs/spherical-video-rfc.md) and
[spatial audio](../docs/spatial-audio-rfc.md)) metadata in MP4 and MOV files.
It can be used to inject spatial media metadata into a file or validate metadata
in an existing file.

# Usage

Go to the releases page and decide between the GUI and CLI version. Download it and unzip it to your desired location.


## CLI Usage

The CLI version can be used from the command line and has the following functions

#### Examine

    python spatialmedia <files...>

For each file specified, prints spatial media metadata contained in the file.

#### Inject

    python spatialmedia -i [--stereo=(none|top-bottom|left-right)] [--spatial-audio] <input> <output>

Saves a version of `<input>` injected with spatial media metadata to `<output>`.
`<input>` and `<output>` must not be the same file.

##### --stereo

Selects the left/right eye frame layout; see the `StereoMode` element in the
[Spherical Video RFC](../docs/spherical-video-rfc.md) for more information.

Options:

- `none`: Mono frame layout.

- `top-bottom`: Top half contains the left eye and bottom half contains the
right eye.

- `left-right`: Left half contains the left eye and right half contains the
right eye.

##### --spatial-audio

Enables injection of spatial audio metadata. If enabled, the file must contain a
4-channel first-order ambisonics audio track with ACN channel ordering and SN3D
normalization; see the [Spatial Audio RFC](../docs/spatial-audio-rfc.md) for
more information.

## Compile instructions

You can of course also compile the GUI and CLI program yourself. For that you need to do the following steps.

1. Clone or download the repository
2. From the top folder (where the setup.py file is present) open a terminal and run

    ```
    pip install .
    ```   

3. Install nuitka:

    ```
    pip install nuitka
    ```

4. Compile the programs. For the CLI version execute the following command from the top folder:

    ```
    python -m nuitka cli_wrapper.py
    ```

   For the GUI version navigate to the spatialmedia folder and execute:

    ```
    python -m nuitka gui.py
    ```

The executables will be placed in a folder called \{filename\}.dist respectively.