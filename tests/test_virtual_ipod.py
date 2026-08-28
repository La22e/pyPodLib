"""Virtual iPod behaviors — seeded folders usable as test fixtures."""

import json

import pytest

from pypodlib.device import (
    ChecksumType,
    available_virtual_ipod_models,
    create_virtual_ipod,
    detect_checksum_type,
    get_firewire_id,
    has_virtual_ipod_info,
    identify_ipod_at_path,
    load_virtual_ipod_info,
)


def test_create_virtual_ipod_seeds_identity_and_layout(tmp_path) -> None:
    device = create_virtual_ipod(tmp_path, "MC297")

    assert has_virtual_ipod_info(tmp_path)
    assert (tmp_path / "iPod_Control" / "Device" / "SysInfo").exists()
    assert (tmp_path / "iPod_Control" / "Device" / "HashInfo").exists()
    assert (tmp_path / "iPod_Control" / "iTunes").is_dir()
    assert (tmp_path / "iPod_Control" / "iTunes" / "iTunesDB").exists()
    assert (tmp_path / "iPod_Control" / "Music").is_dir()
    assert (tmp_path / "iPod_Control" / "Artwork").is_dir()

    payload = json.loads((tmp_path / "iPodInfo.json").read_text())
    assert payload["model_number"] == "MC297"
    assert payload["model_family"] == "iPod Classic"
    assert payload["generation"] == "7th Gen"

    assert device.model_number == "MC297"
    assert device.serial.endswith(payload["serial_suffix"])
    assert device.firewire_id_bytes == bytes.fromhex(payload["firewire_guid"])
    assert device.checksum_type == ChecksumType.HASH58
    assert device.volume_identity_key.startswith("virtual|")


def test_virtual_ipod_loads_through_normal_identification(tmp_path) -> None:
    create_virtual_ipod(tmp_path, "MA005")

    identified = identify_ipod_at_path(str(tmp_path))
    loaded = load_virtual_ipod_info(tmp_path)

    assert identified is not None
    assert identified.model_number == loaded.model_number == "MA005"
    assert identified.serial == loaded.serial
    assert detect_checksum_type(str(tmp_path)) == ChecksumType.NONE
    assert get_firewire_id(str(tmp_path)) == loaded.firewire_id_bytes


@pytest.mark.parametrize(
    "model, expected_db_name",
    [
        ("MC297", "iTunesDB"),
        ("MC060", "iTunesCDB"),  # iPod Nano 5G uses iTunesCDB
        ("MC525", "iTunesCDB"),
    ],
)
def test_create_virtual_ipod_uses_device_database_filename(
    tmp_path, model, expected_db_name,
) -> None:
    create_virtual_ipod(tmp_path, model)
    assert (tmp_path / "iPod_Control" / "iTunes" / expected_db_name).exists()


def test_virtual_ipod_identification_repairs_missing_database(tmp_path) -> None:
    create_virtual_ipod(tmp_path, "MC297")
    db_path = tmp_path / "iPod_Control" / "iTunes" / "iTunesDB"
    db_path.unlink()

    identified = identify_ipod_at_path(str(tmp_path))

    assert identified is not None
    assert db_path.exists()


def test_available_virtual_ipod_models_have_known_serial_suffixes() -> None:
    rows = available_virtual_ipod_models()
    assert rows
    assert all(row["model_number"] and row["serial_suffix"] for row in rows)
    assert any(row["model_number"] == "MC297" for row in rows)
    assert any("Nano" in row["model_family"] for row in rows)