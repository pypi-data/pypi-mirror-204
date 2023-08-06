import typing
import logging
from pathlib import Path

from cpmax_toolbox.file_repair import repair_file, parse_path

import pandas as pd
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("pdf")
from rich.progress import track


def filter_measurement(
    df: pd.DataFrame, fs=500, n_min: float = 0, n_max: float = 100, thres: float = 5000
) -> pd.DataFrame:
    logging.info(
        f"filtering with fs: {fs}Hz, rpm_min: {n_min:.2f} rpm, rpm_max: {n_max:.2f} rpm and a threshold of {thres:.2f} mm/s²"
    )

    def filt_ax(df):
        hit_thres = False
        for col in df.columns:
            hit_thres = hit_thres or (
                ((df[col].max() - df[col].mean()) > thres)
                or ((df[col].mean() - df[col].min()) > thres)
            )

        n = 60 * fs / len(df)
        out_of_nrange = n < n_min or n > n_max

        df["okay"] = 1 - (hit_thres or out_of_nrange)
        return df

    df_temp = df.copy()

    """ remove rotations where any max > thres """
    df_temp["Revolutions"] = (df_temp["Trigger"].diff() < 0).cumsum()
    logging.info(f"found {df_temp['Revolutions'].max()} revolutions, filtering now...")
    df_temp["okay"] = False
    revs_unfilt = (df_temp["Trigger"].diff() < 0).sum()
    dfs = df_temp.groupby("Revolutions", group_keys=True).apply(filt_ax)
    df_temp = dfs.reset_index(drop=True)
    revs_filt = (df_temp["Trigger"].diff() < 0).sum()
    logging.info(f"filtering completed, kept {revs_filt}/{revs_unfilt} Revolutions")
    return df_temp[df_temp["okay"].astype(bool)].reset_index(drop=True)[
        ["Axial", "Radial", "Torsional", "Trigger"]
    ]  # type:ignore - suppress type error from pylance


def calculate_angle_dependency(
    df: typing.Union[pd.DataFrame, Path, str],
    remove_mean: bool = True,
    angle_points=512,
    show_track=False,
) -> pd.DataFrame:
    logging.info(f"calculating angle dependency!")
    logging.debug(
        f"df: {str(type(df))}, remove_mean: {remove_mean},angle_points: {angle_points}, show_track: {show_track}"
    )
    if isinstance(df, str):
        logging.info(f"got string input, parsing to path...")
        df = parse_path(df)

    if isinstance(df, Path):
        logging.info(f"got path input, reading csv...")
        try:
            df = pd.read_csv(df, skiprows=3, sep="\t")
        except:
            logging.warn(
                f"file {str(df)} is not a viba import file! trying to repair..."
            )
            df = pd.read_csv(repair_file(df), skiprows=3, sep="\t")

    means = {c: df[c].mean() for c in df.columns}
    logging.debug(
        f"len(df): {len(df)}, df.columns: {', '.join(list(df.columns))}, means: {means}"
    )

    col_soll = {"Axial", "Radial", "Torsional", "Trigger"}
    col_ist = set(df.columns)
    if col_ist != col_soll:
        logging.warn(
            f"columns in Dataframe not matching {{{', '.join(col_soll)}}}, trying anyways"
        )
        # raise ValueError(f"columns in Dataframe not matching {{{', '.join(col_soll)}}}")

    df_temp = df.copy()
    if remove_mean:
        for ax in ["Axial", "Radial", "Torsional"]:
            df_temp[ax] = df_temp[ax] - df_temp[ax].mean()

    df_temp["Revolutions"] = (df_temp["Trigger"].diff() < 0).cumsum()
    dfs = []

    if show_track:
        gen = lambda x: track(x, "calculating angle dependency...")
    else:
        gen = lambda x: x

    logging.info("calculating angle dependency...")
    for i in gen(range(df_temp["Revolutions"].max())):
        dfi = df_temp[df_temp["Revolutions"] == i]
        logging.debug(f"i: {i}, len(dfi): {len(dfi)}")
        keys = ["Axial", "Radial", "Torsional", "Trigger"]
        data = {}
        for k in keys:
            if k == "Trigger":
                data[k] = ((angle_points - 1) * [0]) + [1]
            else:
                data[k] = signal.resample(dfi[k], angle_points)

        dfs.append(pd.DataFrame(data))
    logging.debug("done! concating...")
    df_temp = pd.concat(dfs, ignore_index=True)
    logging.info(f"done!")
    return df_temp


def create_specs(
    df_meas: pd.DataFrame,
    output_pdf: typing.Union[Path, None] = None,
    prefix: str = "",
    fs: int = 512,
    xmin: float = 0,
    xmax: float = 5,
) -> None:
    """fft calculation and plot -> vibA design"""
    # fft_freqs = np.fft.fftfreq(int(len(df_meas)), 1/fs)[: len(df_meas) // 2]
    logging.info("creating spec")
    logging.debug(
        f"len(df_meas): {len(df_meas)}, output_pdf: {output_pdf}, prefix: {prefix}, fs: {fs}, xmin: {xmin}, xmax: {xmax}"
    )
    data = {"f": np.fft.fftfreq(int(len(df_meas)), 1 / fs)[: len(df_meas) // 2]}
    for ax in ["Axial", "Radial"]:
        logging.debug(f"calulating fft of {ax}")
        data[ax] = (
            2 * np.abs(np.fft.fft(df_meas[ax]))[: len(df_meas) // 2] / len(df_meas)
        )
    logging.debug(f"done!")

    df_fft = pd.DataFrame(data=data)

    fig, axs = plt.subplots(2, 1, sharey=True)
    colors = ["#ffa500", "#9acd32"]
    r_max = df_fft[np.abs(df_fft["f"] - 1) < df_fft["f"][1]].max()
    ymax = 5*((max([r_max['Axial'], r_max['Radial']])//5)+1)

    for i, ax in enumerate(["Axial", "Radial"]):
        logging.debug(f"creating plot of {ax}")
        axs[i].plot(df_fft["f"], df_fft[ax], label=ax, color=colors[i])
        axs[i].axis(xmin=xmin, xmax=xmax, ymin=0, ymax=ymax)
        axs[i].set_xlabel("Order / Frequency [Hz]")
        axs[i].set_ylabel("Amplitude [mm/s²]")
        axs[i].grid()
        axs[i].legend(loc="upper right")
        logging.debug(f"done")

    logging.info(
        f"1P Values: Axial: {r_max['Axial']:.2f}mm/s², Radial: {r_max['Radial']:.2f}mm/s²"
    )
    if output_pdf:
        fig.set_size_inches(10, 10)

        if output_pdf.is_dir():
            output_pdf = output_pdf / (
                prefix
                + f"__res_{df_fft['f'][1]:.5f}P__Ax_{r_max['Axial']:.2f}mms2__Rad_{r_max['Radial']:.2f}mms2.pdf"
            )

        logging.info(f"saving plot to {output_pdf}")
        fig.savefig(
            output_pdf,  # type:ignore - suppress pylint warning message (Path -> str not compatible)
            bbox_inches="tight",
            dpi=600,
        )
    else:
        plt.show()

# create a function prototype