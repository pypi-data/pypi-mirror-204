Interfaces for HTTP API <a href="https://kabinet.pecom.ru/api/v1">PECOM</a> transport company.
Usage:

from promsoft_pecom_interface import IdentityCard


ic = IdentityCard(series='1234', numbers='567890')
print(f"As dict: {ic.dict()}")