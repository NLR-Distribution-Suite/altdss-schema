import opendssdirect as dss
import pytest

from altdss_schema.altdss_models import Transformer, XfmrCode


@pytest.mark.parametrize("model", [Transformer, XfmrCode])
@pytest.mark.parametrize("resistances", [[0.2, 0.6], [0.266272, 0.532544, 0.532544]])
@pytest.mark.parametrize("edit", [False, True])
def test_explicit_winding_resistances_override_total_load_loss(
    model, resistances, edit
):
    count = len(resistances)
    fields = {
        "Name": "test",
        "Phases": 1,
        "kV": [12.47] + [0.12] * (count - 1),
        "kVA": [50] * count,
        "Conn": ["wye"] * count,
        "pctR": resistances,
        "pctLoadLoss": sum(resistances[:2]),
        "X12": 2.4,
    }
    if model is Transformer:
        fields["Bus"] = ["source.1", "secondary.1"] + (
            ["secondary.2"] if count == 3 else []
        )
    dss.Basic.ClearAll()
    dss.Text.Command("new circuit.test")
    if edit:
        dss.Text.Command(model.dict_dumps_dss(fields).strip())
    command = model.dict_dumps_dss(fields, edit=edit)
    assert command.index("%LoadLoss=") < command.index("%Rs=")
    dss.Text.Command(command.strip())
    dss.Text.Command(f"? {model.__name__}.test.%rs")
    actual = [
        float(value)
        for value in dss.Text.Result().strip("[] ").split(",")
        if value.strip()
    ]
    assert actual == pytest.approx(resistances)


@pytest.mark.parametrize("model", [Transformer, XfmrCode])
def test_total_load_loss_without_explicit_resistances(model):
    fields = {"Name": "test", "Phases": 1, "kV": [12.47, 0.12], "pctLoadLoss": 0.8}
    if model is Transformer:
        fields["Bus"] = ["source.1", "secondary.1"]
    command = model.dict_dumps_dss(fields)
    assert "%LoadLoss=0.8" in command
    assert "%Rs=" not in command
