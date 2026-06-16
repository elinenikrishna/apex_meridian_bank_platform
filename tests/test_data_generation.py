from pathlib import Path

from apex_meridian.data_generation.generator import write_domain_csv


def test_generator_writes_batched_transaction_data(tmp_path: Path):
    paths = write_domain_csv("transactions", tmp_path, records=25, batch_size=10, seed=7)
    assert len(paths) == 3
    assert paths[0].read_text(encoding="utf-8").splitlines()[0].startswith("transaction_id")


def test_generator_supports_account_balance_domain(tmp_path: Path):
    paths = write_domain_csv("account_balances", tmp_path, records=3, batch_size=2, seed=11)
    header = paths[0].read_text(encoding="utf-8").splitlines()[0]
    assert "ledger_balance" in header
