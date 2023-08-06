from __future__ import annotations

import json
import math
from pathlib import Path

import itkdb
import pandas as pd
import typer

import module_qc_database_tools

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})


@app.command()
def main(
    serial_number: str = typer.Option(..., "-sn", "--sn", help="ATLAS serialNumber"),
    chip_template: Path = typer.Option(
        (module_qc_database_tools.data / "YARR" / "chip_template.json").resolve(),
        "-ch",
        "--chipTemplate",
        help="Default chip template from which the chip configs are generated.",
        exists=True,
        file_okay=True,
        readable=True,
        resolve_path=True,
    ),
    output_dir: Path = typer.Option(
        ...,
        "-o",
        "--outdir",
        help="Path to output directory. Configs must be in Yarr/configs.",
        exists=False,
        writable=True,
    ),
):
    """
    Main executable for generating yarr config.
    """
    client = itkdb.Client()
    module = Module(client, serial_number)
    typer.echo("INFO: Getting layer-dependent config from module SN...")
    layer_config = get_layer_from_serial_number(serial_number)

    module.generate_config(chip_template, output_dir, layer_config, suffix="warm")
    module.generate_config(chip_template, output_dir, layer_config, suffix="cold")
    module.generate_config(chip_template, output_dir, layer_config, suffix="LP")


class Module:
    """
    Module class.
    """

    def __init__(self, client, serial_number, name=None):
        self.client = client
        self.serial_number = serial_number
        self.name = name if name else self.serial_number
        self.module = client.get("getComponent", json={"component": serial_number})
        self.bare_modules = []
        for child in self.module["children"]:
            if child["componentType"]["code"] == "BARE_MODULE":
                self.bare_modules.append(
                    client.get(
                        "getComponent",
                        json={"component": child["component"]["serialNumber"]},
                    )
                )
        self.chips = []
        for bare_module in self.bare_modules:
            for child in bare_module["children"]:
                if child["componentType"]["code"] == "FE_CHIP":
                    self.chips.append(
                        Chip(
                            client,
                            child["component"]["serialNumber"],
                            module_name=self.name,
                        )
                    )
        if len(self.bare_modules) == 3 and len(self.chips) == 3:
            self.module_type = "triplet"
            typer.echo(f"INFO: triplet {self.serial_number} initiated.")
        else:
            self.module_type = "quad"
            typer.echo(f"INFO: quad module {self.serial_number} initiated.")

    def generate_config(self, chip_template, outdir, layer_config, suffix):
        """
        Generate module config.
        """
        typer.echo(
            f"INFO: generating module config for module {self.serial_number} with {layer_config}"
        )

        spec = {"chipType": "RD53B", "chips": []}

        for chip_index, chip in enumerate(self.chips):
            if self.module_type == "triplet":
                spec["chips"].append(
                    {
                        "config": chip.generate_config(
                            chip_template,
                            outdir,
                            chip_index,
                            layer_config,
                            self.module_type,
                            suffix=suffix,
                        ),
                        "path": "relToCon",
                        "tx": 0,
                        "rx": [0, 1, 2][chip_index],
                        "enable": 1,
                        "locked": 0,
                    }
                )
            else:
                spec["chips"].append(
                    {
                        "config": chip.generate_config(
                            chip_template,
                            outdir,
                            chip_index,
                            layer_config,
                            self.module_type,
                            suffix=suffix,
                        ),
                        "path": "relToCon",
                        "tx": 0,
                        "rx": [2, 1, 0, 3][chip_index],
                        "enable": 1,
                        "locked": 0,
                    }
                )

        output_path = Path(outdir, self.name)
        output_path.mkdir(parents=True, exist_ok=True)
        with output_path.joinpath(
            f"{self.name}_{layer_config}{'_'+suffix if suffix else ''}.json"
        ).open("w", encoding="utf-8") as serialized:
            json.dump(spec, serialized, indent=4)
        typer.echo(
            f"INFO: connectivity file saved to {outdir}/{self.name}/{self.name}_{layer_config}{'_'+suffix if suffix else ''}.json"
        )


class Chip:
    """
    Chip class.
    """

    def __init__(self, client, serial_number, module_name=None):
        self.client = client
        self.serial_number = serial_number
        self.chip_uid = hex(int(serial_number[-7:]))
        self.module_name = module_name or self.serial_number
        self.chip = client.get("getComponent", json={"component": serial_number})
        self.test_run = None

        typer.echo(f"INFO: chip {self.chip_uid} initiated.")

    def load_wafer_probing_data(self):
        """
        Load chip wafer probing data.
        """
        test_id = None
        tests = pd.DataFrame(self.chip["tests"])
        if len(tests[tests["code"] == "FECHIP_TEST"]) > 0:
            test_id = tests[tests["code"] == "FECHIP_TEST"]["testRuns"].iloc[-1][-1][
                "id"
            ]
        if not test_id:
            msg = (
                f"No wafer probing data in production DB for chip {self.serial_number}!"
            )
            raise RuntimeError(msg)
        self.test_run = TestRun(self.client, test_id)

    def generate_config(
        self, chip_template, outdir, chip_index, layer_config, module_type, suffix=""
    ):
        """
        Generate chip config.
        """
        typer.echo(
            f"INFO: generating chip config for chip {self.chip_uid} with {layer_config}"
        )

        with Path(chip_template).open(encoding="utf-8") as serialized:
            spec = json.load(serialized)

        power_config = "LP" if suffix == "LP" else layer_config

        spec["RD53B"]["GlobalConfig"]["DiffPreComp"] = {
            "R0": 350,
            "R0.5": 350,
            "L0": 350,
            "L1": 350,
            "L2": 350,
            "LP": 0,
        }[power_config]
        spec["RD53B"]["GlobalConfig"]["DiffPreampL"] = {
            "R0": 900,
            "R0.5": 900,
            "L0": 900,
            "L1": 730,
            "L2": 550,
            "LP": 0,
        }[power_config]
        spec["RD53B"]["GlobalConfig"]["DiffPreampM"] = {
            "R0": 900,
            "R0.5": 900,
            "L0": 900,
            "L1": 730,
            "L2": 550,
            "LP": 0,
        }[power_config]
        spec["RD53B"]["GlobalConfig"]["DiffPreampR"] = {
            "R0": 900,
            "R0.5": 900,
            "L0": 900,
            "L1": 730,
            "L2": 550,
            "LP": 0,
        }[power_config]
        spec["RD53B"]["GlobalConfig"]["DiffPreampT"] = {
            "R0": 900,
            "R0.5": 900,
            "L0": 900,
            "L1": 730,
            "L2": 550,
            "LP": 0,
        }[power_config]
        spec["RD53B"]["GlobalConfig"]["DiffPreampTL"] = {
            "R0": 900,
            "R0.5": 900,
            "L0": 900,
            "L1": 730,
            "L2": 550,
            "LP": 0,
        }[power_config]
        spec["RD53B"]["GlobalConfig"]["DiffPreampTR"] = {
            "R0": 900,
            "R0.5": 900,
            "L0": 900,
            "L1": 730,
            "L2": 550,
            "LP": 0,
        }[power_config]
        spec["RD53B"]["GlobalConfig"]["DiffVff"] = {
            "R0": 150,
            "R0.5": 150,
            "L0": 150,
            "L1": 150,
            "L2": 60,
            "LP": 0,
        }[power_config]
        spec["RD53B"]["GlobalConfig"]["EnCoreCol0"] = {
            "R0": 65535,
            "R0.5": 65535,
            "L0": 65535,
            "L1": 65535,
            "L2": 65535,
            "LP": 0,
        }[power_config]
        spec["RD53B"]["GlobalConfig"]["EnCoreCol1"] = {
            "R0": 65535,
            "R0.5": 65535,
            "L0": 65535,
            "L1": 65535,
            "L2": 65535,
            "LP": 0,
        }[power_config]
        spec["RD53B"]["GlobalConfig"]["EnCoreCol2"] = {
            "R0": 65535,
            "R0.5": 65535,
            "L0": 65535,
            "L1": 65535,
            "L2": 65535,
            "LP": 0,
        }[power_config]
        spec["RD53B"]["GlobalConfig"]["EnCoreCol3"] = {
            "R0": 63,
            "R0.5": 63,
            "L0": 63,
            "L1": 63,
            "L2": 63,
            "LP": 0,
        }[power_config]
        spec["RD53B"]["Parameter"]["Name"] = self.chip_uid

        if module_type == "triplet":
            spec["RD53B"]["Parameter"]["ChipId"] = chip_index + 1
            spec["RD53B"]["GlobalConfig"]["AuroraActiveLanes"] = {
                "R0": 7,
                "R0.5": 3,
                "L0": 15,
            }[
                layer_config
            ]  ## TODO: add source for R0 and R0.5
            # spec["RD53B"]["GlobalConfig"]["MonitorEnable"] = 0
            # spec["RD53B"]["GlobalConfig"]["MonitorV"] = 63
            for index in range(4):
                spec["RD53B"]["GlobalConfig"][f"DataMergeOutMux{index}"] = (
                    0 + index
                ) % 4
            spec["RD53B"]["GlobalConfig"]["SerEnLane"] = {"R0": 7, "R0.5": 3, "L0": 15}[
                layer_config
            ]
        else:
            spec["RD53B"]["Parameter"]["ChipId"] = 12 + chip_index
            spec["RD53B"]["GlobalConfig"]["AuroraActiveLanes"] = 1
            for index in range(4):
                spec["RD53B"]["GlobalConfig"][f"DataMergeOutMux{index}"] = (
                    [2, 0, 1, 0][chip_index] + index
                ) % 4
            spec["RD53B"]["GlobalConfig"]["SerEnLane"] = [4, 1, 8, 1][chip_index]

        if not self.test_run:
            self.load_wafer_probing_data()
        if self.test_run:
            spec["RD53B"]["GlobalConfig"]["SldoTrimA"] = self.test_run.get_result(
                "VDDA_TRIM"
            )
            spec["RD53B"]["GlobalConfig"]["SldoTrimD"] = self.test_run.get_result(
                "VDDD_TRIM"
            )
            spec["RD53B"]["Parameter"]["ADCcalPar"][0] = (
                self.test_run.get_result("ADC_OFFSET") * 1000
            )
            spec["RD53B"]["Parameter"]["ADCcalPar"][1] = (
                self.test_run.get_result("ADC_SLOPE") * 1000
            )
            spec["RD53B"]["Parameter"]["InjCap"] = self.test_run.get_result(
                "InjectionCapacitance"
            ) * (10**15)

            # For transistor sensors calibration, the ideality factor is calculated following the presentation:
            # https://indico.cern.ch/event/1011941/contributions/4278988/attachments/2210633/3741190/RD53B_calibatrion_sensor_temperature.pdf
            e_charge = 1.602e-19
            kB = 1.38064852e-23
            PC_NTC = self.test_run.get_result("PC_NTC") + 273
            DeltaT = 2  # 2 degree difference between PC NTC and transistor sensors
            spec["RD53B"]["Parameter"]["NfDSLDO"] = (
                self.test_run.get_result("TEMPERATURE_D")
                * e_charge
                / (kB * math.log(15) * (PC_NTC + DeltaT))
            )
            spec["RD53B"]["Parameter"]["NfASLDO"] = (
                self.test_run.get_result("TEMPERATURE_A")
                * e_charge
                / (kB * math.log(15) * (PC_NTC + DeltaT))
            )
            spec["RD53B"]["Parameter"]["NfACB"] = (
                self.test_run.get_result("TEMPERATURE_C")
                * e_charge
                / (kB * math.log(15) * (PC_NTC + DeltaT))
            )

            spec["RD53B"]["Parameter"]["VcalPar"] = [
                abs(self.test_run.get_result("VCAL_HIGH_LARGE_RANGE_OFFSET") * 1000),
                self.test_run.get_result("VCAL_HIGH_LARGE_RANGE_SLOPE") * 1000,
            ]
            spec["RD53B"]["Parameter"]["IrefTrim"] = self.test_run.get_result(
                "IREF_TRIM"
            )
            spec["RD53B"]["Parameter"]["KSenseInA"] = self.test_run.get_result(
                "CURR_MULT_FAC_A"
            )
            spec["RD53B"]["Parameter"]["KSenseInD"] = self.test_run.get_result(
                "CURR_MULT_FAC_D"
            )
            spec["RD53B"]["Parameter"]["KSenseShuntA"] = (
                self.test_run.get_result("CURR_MULT_FAC_A") * 26000.0 / 21000.0
            )
            spec["RD53B"]["Parameter"]["KSenseShuntD"] = (
                self.test_run.get_result("CURR_MULT_FAC_D") * 26000.0 / 21000.0
            )
            spec["RD53B"]["Parameter"]["KShuntA"] = self.test_run.get_result(
                "VINA_SHUNT_KFACTOR"
            )
            spec["RD53B"]["Parameter"]["KShuntD"] = self.test_run.get_result(
                "VIND_SHUNT_KFACTOR"
            )

        output_path = Path(
            outdir, self.module_name, f"{layer_config}{'_'+suffix if suffix else ''}"
        )
        output_path.mkdir(parents=True, exist_ok=True)
        output_file = output_path.joinpath(
            f"{self.chip_uid}_{layer_config}{'_'+suffix if suffix else ''}.json"
        )
        with output_file.open("w", encoding="utf-8") as serialized:
            json.dump(spec, serialized, indent=4)

        typer.echo(f"INFO: chip config saved to {output_file}")
        return str(Path(*output_file.parts[-2:]))


class TestRun:
    """
    TestRun class.
    """

    def __init__(self, client, test_run_id):
        self.client = client
        self.identifier = test_run_id
        self.test_run = client.get("getTestRun", json={"testRun": test_run_id})
        self.results = pd.DataFrame(self.test_run["results"])

        typer.echo(f"INFO: test run {self.identifier} initiated.")

    def get_result(self, code):
        """
        Get test run result.
        """
        if len(self.results[self.results["code"] == code]) > 0:
            return self.results[self.results["code"] == code]["value"].iloc[-1]
        return None


def get_layer_from_serial_number(serial_number):
    """
    Get the layer from the serial number.
    """
    if len(serial_number) != 14 or not serial_number.startswith("20U"):
        typer.echo("Error: Please enter a valid ATLAS SN.")
        raise typer.Exit(code=1)

    if "PIMS" in serial_number or "PIR6" in serial_number:
        return "L0"

    if "PIM0" in serial_number or "PIR7" in serial_number:
        return "R0"

    if "PIM5" in serial_number or "PIR8" in serial_number:
        return "R0.5"

    if "PIM1" in serial_number or "PIRB" in serial_number:
        return "L1"

    if "PG" in serial_number:
        return "L2"

    typer.echo("Error: invalid module SN.")
    raise typer.Exit(code=1)


if __name__ == "__main__":
    typer.run(main)
