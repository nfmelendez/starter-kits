from forta_agent import FindingSeverity, create_transaction_event

import agent
from web3_mock import (BENIGN_CONTRACT, CONTRACT_NO_ADDRESS,
                       CONTRACT_WITH_ADDRESS, CONTRACT_WITH_METADATA,
                       CONTRACT_WITHOUT_METADATA, EOA_ADDRESS,
                       MALICIOUS_CONTRACT, MALICIOUS_CONTRACT_DEPLOYER,
                       MALICIOUS_CONTRACT_DEPLOYER_NONCE, SHORT_CONTRACT,
                       Web3Mock)

w3 = Web3Mock()


class TestMaliciousSmartContractML:
    def test_is_contract_eoa(self):
        assert not agent.is_contract(w3, EOA_ADDRESS), "EOA shouldn't be identified as a contract"

    def test_is_contract_contract(self):
        assert agent.is_contract(w3, CONTRACT_NO_ADDRESS), "Contract should be identified as a contract"

    def test_has_metadata_has(self):
        assert agent.has_metadata(w3, w3.eth.get_code(CONTRACT_WITH_METADATA)), "Contract has no metadata"

    def test_has_metadata_none(self):
        assert not agent.has_metadata(w3, w3.eth.get_code(CONTRACT_WITHOUT_METADATA)), "Contract has no metadata"

    def test_get_opcode_addresses_eoa(self):
        addresses = agent.get_opcode_addresses(w3, w3.eth.get_code(EOA_ADDRESS))
        assert len(addresses) == 0, "should be empty"

    def test_get_opcode_addresses_no_addr(self):
        addresses = agent.get_opcode_addresses(w3, w3.eth.get_code(CONTRACT_NO_ADDRESS))
        assert len(addresses) == 0, "should not be empty"

    def test_get_opcode_addresses_with_addr(self):
        addresses = agent.get_opcode_addresses(w3, w3.eth.get_code(CONTRACT_WITH_ADDRESS))
        assert len(addresses) == 1, "should not be empty"

    def test_storage_addresses_with_addr(self):
        addresses = agent.get_opcode_addresses(w3, w3.eth.get_code(CONTRACT_WITH_ADDRESS))
        assert len(addresses) == 1, "should not be empty"

    def test_storage_addresses_on_eoa(self):
        addresses = agent.get_opcode_addresses(w3, w3.eth.get_code(EOA_ADDRESS))
        assert len(addresses) == 0, "should be empty; EOA has no storage"

    def test_calc_contract_address(self):
        contract_address = agent.calc_contract_address(w3, EOA_ADDRESS, 9)
        assert contract_address == "0x728ad672409DA288cA5B9AA85D1A55b803bA97D7", "should be the same contract address"

    def test_get_features(self):
        hashes = agent.get_features(w3, w3.eth.get_code(MALICIOUS_CONTRACT))
        assert len(hashes) == 18, "incorrect number of functions obtained"

    def test_finding_malicious_contract_creation(self):
        agent.initialize()

        tx_event = create_transaction_event({
            'transaction': {
                'hash': "0",
                'from': MALICIOUS_CONTRACT_DEPLOYER,
                'nonce': MALICIOUS_CONTRACT_DEPLOYER_NONCE,
            },
            'block': {
                'number': 0
            },
            'traces': [
                 {'type': 'create',
                 'action': {
                     'from': MALICIOUS_CONTRACT_DEPLOYER,
                     'value': 1,
                 }
                 }
            ],
            'receipt': {
                'logs': []}
        })
        findings = agent.detect_malicious_contract_creations(w3, tx_event)
        assert len(findings) == 1, "this should have triggered a finding"
        finding = next((x for x in findings if x.alert_id == 'SUSPICIOUS-CONTRACT-CREATION'), None)
        assert finding.severity == FindingSeverity.High

    def test_detect_malicious_contract_benign(self):
        agent.initialize()
        findings = agent.detect_malicious_contract(w3, EOA_ADDRESS, BENIGN_CONTRACT)
        assert len(findings) == 0, "this should not have triggered a finding"

    def test_detect_malicious_contract_short(self):
        agent.initialize()
        findings = agent.detect_malicious_contract(w3, EOA_ADDRESS, SHORT_CONTRACT)
        assert len(findings) == 0, "this should not have triggered a finding"
