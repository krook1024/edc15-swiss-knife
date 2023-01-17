#!/usr/bin/env python3

import PySimpleGUI as sg
import tools.ols_converter as oc
from tools.convert import excel_to_edc
from tools.extrapolation import extrapolate


def edc_2_ols(file: str) -> None:
    print(f"converting {file} to ols json")
    json = oc.get_json_as_olscollection(file)
    filename = sg.popup_get_file(
        "Select the target destination", multiple_files=False, save_as=True, no_window=True,
        file_types=(("JSON", "*.json"),), default_extension="json")

    if len(filename.strip()) > 0:
        with open(filename, 'w') as f:
            f.write(json)


def extrapolation(headers: str, target: str, values: str, window) -> None:
  source=[int(x) for x in headers.split(',')]
  print(source)
  result = extrapolate(
    source=[int(x) for x in headers.split(',')],
    target=[int(x) for x in target.split(',')],
    values=values
  )
  window['-extrapolationResult-'].update(result, visible=True)
  window['-extrapolationResultText-'].update(visible=True)


def main():
    converter_layout = [
        [
            sg.Text("Choose a file to get JSON maplist for WinOLS:"),
            sg.FileBrowse(target="-fileToConvert-", file_types=(("Binaries", "*.mod *.bin *.ori"),)),
            sg.Text(key="-fileToConvert-"),
        ], [sg.Button("Convert", key="convert_edc2json")]
    ]

    extrapolation_layout = [
        [sg.Text("Headers (for example: 55,60):", size=(22, None)), sg.InputText(key="-headerValues-")],
        [sg.Text("Target (for example: 70):", size=(22, None)), sg.InputText(key="-targetValue-")],
        [sg.Text("Values:", size=(22, None)), sg.InputText(key="-values-")],
        [sg.Button("Extrapolate", key="extrapolate")],
        [sg.Text("Result:", key="-extrapolationResultText-", visible=False)],
        [sg.Multiline("", key="-extrapolationResult-", disabled=True, visible=False, expand_x=True, expand_y=True)],
    ]

    clipboard_layout = [
        [sg.Button("Convert from Excel to EDCSuite format", key="convert_excel2edc")]
    ]

    diffmap_layout = [
        [sg.Text("First map:", size=(22, None)), sg.InputText(key="-firstMap-")],
        [sg.Text("Second map:", size=(22, None)), sg.InputText(key="-secondMap-")],
        [sg.Text("Note: Maps have to be equal in size!")],
        [sg.Button("Calculate", key="diffmap")],
    ]

    layout = [[sg.TabGroup(
        [[
            sg.Tab('EDC2OLS', converter_layout, key="-converterTab-"),
            sg.Tab('Extrapolation', extrapolation_layout, key="-extrapolationTab-"),
            sg.Tab('Clipboard tools', clipboard_layout, key="-clipboardTab-"),
            sg.Tab('Difference map calculator', diffmap_layout, key="-diffMapTab-"),
        ]], border_width=1, expand_y=True, expand_x=True)
    ]]
    window = sg.Window(title="Swiss Knife for EDC15",
                       layout=layout, size=(800, 300))

    while True:
        event, values = window.read()

        print(values)

        try:
            if event == sg.WIN_CLOSED:
                break
            elif event == "convert_edc2json":
                if 'Browse' in values and len(values['Browse'].strip()) > 0:
                    edc_2_ols(values['Browse'])
            elif event == "convert_excel2edc":
              excel_to_edc()
            elif event == "diffmap":
                pass
            elif event == "extrapolate":
                if all((k in values and len(values[k].strip()) > 0) for k in ("-headerValues-", "-targetValue-", "-values-")):
                     extrapolation(values['-headerValues-'], values['-targetValue-'], values['-values-'], window)
        except Exception as e:
            print(e)
            sg.popup(f"An error happened!\n{str(e)}", title="Error")


if __name__ == "__main__":
    main()
