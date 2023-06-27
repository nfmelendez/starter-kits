import time
import timeit
import os
import io
import random
import base64
import gnupg
from datetime import datetime
import pandas as pd
import numpy as np
from forta_agent import create_transaction_event, create_alert_event, FindingSeverity, AlertEvent, Label, EntityType, Finding, FindingType
import requests
import agent

from constants import BASE_BOTS, MODEL_ALERT_THRESHOLD_LOOSE, MODEL_FEATURES
from web3_mock import CONTRACT, EOA_ADDRESS_SMALL_TX, Web3Mock, EOA_ADDRESS_LARGE_TX, CONTRACT2
from forta_explorer_mock import FortaExplorerMock
from blockchain_indexer_mock import BlockChainIndexerMock
from utils import Utils

w3 = Web3Mock()
forta_explorer = FortaExplorerMock()
block_chain_indexer = BlockChainIndexerMock()


class TestScamDetector:

    @staticmethod
    def encrypt_alert_event(alert_event: AlertEvent):
        public_key = """-----BEGIN PGP PUBLIC KEY BLOCK-----

            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
            =QBhA
            -----END PGP PUBLIC KEY BLOCK-----
            """
        gpg = gnupg.GPG(gnupghome='.')
        import_result = gpg.import_keys(public_key)
        fp = ""
        for fingerprint in import_result.fingerprints:
            fp = fingerprint
            gpg.trust_keys(fingerprint, 'TRUST_ULTIMATE')


        finding = Finding({
            'name': alert_event.alert.name,
            'description': alert_event.alert.description,
            'alert_id': alert_event.alert.alert_id,
            'severity': FindingSeverity(alert_event.alert.severity),
            'type': FindingType(alert_event.alert.finding_type),
            'metadata': alert_event.alert.metadata,
            'labels': alert_event.alert.labels,
        })
        finding_json = finding.toJson()
        encrypted_finding = gpg.encrypt(finding_json, fp)
        encrypted_finding_ascii = str(encrypted_finding)
        encrypted_finding_base64 = base64.b64encode(encrypted_finding_ascii.encode("utf-8")).decode("utf-8")

        alert_event.alert.name = "omitted"
        alert_event.alert.description = "omitted"
        alert_event.alert.alert_id = "omitted"
        alert_event.alert.severity = FindingSeverity.Unknown
        alert_event.alert.finding_type = FindingType.Unknown
        alert_event.alert.metadata = { 'data': encrypted_finding_base64 }
        alert_event.alert.labels = []
        return alert_event
        

    @staticmethod
    def generate_alert(bot_id: str, alert_id: str, description = "", metadata={}, labels=[], transaction_hash = "0x123", alert_hash = '0xabc', timestamp = 0) -> AlertEvent:
        labels_tmp = [] if len(labels) == 0 else labels
        ts = "2022-11-18T03:01:21.457234676Z" if timestamp == 0 else datetime.fromtimestamp(timestamp).strftime("%Y-%m-%dT%H:%M:%S.%f123Z")  # 2022-11-18T03:01:21.457234676Z
        alert = {"alert":
                  {"name": "x",
                   "hash": alert_hash,
                   "addresses": [],
                   "description": description,
                   "alertId": alert_id,
                   "chainId": 1,
                   "severity": 2,
                   "findingType": 2,  
                   "createdAt": ts,
                   "source": {"bot": {'id': bot_id}, "block": {"chainId": 1, 'number': 5},  'transactionHash': transaction_hash},
                   "metadata": metadata,
                   "labels": labels_tmp
                  }
                }
        
        return create_alert_event(alert)
    
    @staticmethod
    def filter_findings(findings: list, logic: str) -> list:
        findings_result = []
        for finding in findings:
            if 'logic' in finding.metadata.keys() and finding.metadata['logic'] == logic:
                findings_result.append(finding)
        return findings_result

    def test_initialize(self):
        agent.initialize()
        assert agent.INITIALIZED

    # def test_perf_passthrough_alert(self):
    #     global w3
    #     agent.initialize()
    #     agent.item_id_prefix = "test_" + str(random.randint(0, 1000000))

    #     shards = Utils.get_total_shards(1)
        
    #     bot_id = "0x067e4c4f771f288c686efa574b685b98a92918f038a478b82c9ac5b5b6472732"
    #     alert_id = "NFT-WASH-TRADE"
    #     description = "test Wash Trade on test."
    #     metadata = {"buyerWallet":"0xa53496B67eec749ac41B4666d63228A0fb0409cf","sellerWallet":"0xD73e0DEf01246b650D8a367A4b209bE59C8bE8aB","anomalyScore":"21.428571428571427% of total trades observed for test are possible wash trades","collectionContract":"test","collectionName":"test","exchangeContract":"test","exchangeName":"test","token":"Wash Traded NFT Token ID: 666688"}
    #     global wash_trading_alert_event
    #     wash_trading_alert_event = TestScamDetector.generate_alert(bot_id, alert_id, description, metadata)

    #     bot_id = "0xc608f1aff80657091ad14d974ea37607f6e7513fdb8afaa148b3bff5ba305c15"
    #     alert_id = "HARD-RUG-PULL-1"
    #     description = "0x8181bad152a10e7c750af35e44140512552a5cd9 deployed a token contract 0xb68470e3E66862bbeC3E84A4f1993D1d100bc5A9 that may result in a hard rug pull."
    #     metadata = {"attacker_deployer_address":"0x8181bad152a10e7c750af35e44140512552a5cd9","rugpull_techniques":"HIDDENTRANSFERREVERTS, HONEYPOT","token_contract_address":"0xb68470e3E66862bbeC3E84A4f1993D1d100bc5A9"}
    #     global hard_rug_pull_alert_event
    #     hard_rug_pull_alert_event = TestScamDetector.generate_alert(bot_id, alert_id, description, metadata)

    #     bot_id = "0x36be2983e82680996e6ccc2ab39a506444ab7074677e973136fa8d914fc5dd11"
    #     alert_id = "RAKE-TOKEN-CONTRACT-1"
    #     description = "swapExactETHForTokensSupportingFeeOnTransferTokens function detected on Uniswap Router to take additional swap fee."
    #     metadata = {"actualValueReceived":"1.188051244910305019265053e+24","anomalyScore":"0.2226202661207779","attackerRakeTokenDeployer":"0xa0f80e637919e7aad4090408a63e0c8eb07dfa03","feeRecipient":"0x440aeca896009f006eea3df4ba3a236ee8d57d36","from":"0x6c07456233f0e0fd03137d814aacf225f528068d","pairAddress":"0x2b25f23c31a490583ff55fb63cea459c098cc0e8","rakeTokenAddress":"0x440aeca896009f006eea3df4ba3a236ee8d57d36","rakeTokenDeployTxHash":"0xec938601346b2ecac1bd82f7ce025037c09a3d817d00d723efa6fc5507bca5c2","rakedFee":"2.09656102042995003399715e+23","rakedFeePercentage":"15.00","totalAmountTransferred":"1.397707346953300022664768e+24"}
    #     global rake_token_alert_event
    #     rake_token_alert_event = TestScamDetector.generate_alert(bot_id, alert_id, description, metadata)

    #     bot_id = "0xf234f56095ba6c4c4782045f6d8e95d22da360bdc41b75c0549e2713a93231a4"
    #     alert_id = "SOFT-RUG-PULL-SUS-LIQ-POOL-RESERVE-CHANGE && SOFT-RUG-PULL-SUS-LIQ-POOL-CREATION"
    #     description = "Likely Soft rug pull has been detected"
    #     metadata = {"alert_hash":"0xd99ed20f397dbe53721e9a3424d0b87bcffb8df09fc2a9fea5748f81f3c7d324 && 0x0de8a4f6e1efff58a43cb20a81dd491e23b5eea32412a7b679129eb7b0638ea1","alert_id":"SOFT-RUG-PULL-SUS-LIQ-POOL-RESERVE-CHANGE && SOFT-RUG-PULL-SUS-LIQ-POOL-CREATION","bot_id":"0x1a6da262bff20404ce35e8d4f63622dd9fbe852e5def4dc45820649428da9ea1","contractAddress":"\"0x27382445B936C1f362CbBC32E3d3fa5947220030\"","deployer":"\"0xa3fe18ced8d32ca601e3b4794856c85f6f56a176\"","token":"\"0xdd17532733f084ee4aa2de4a14993ef363843216\"","txHashes":"\"0x136af8104791a904614df3728a4bacf3bb79854db362e70f65e64a787ca23efa\""}
    #     global soft_rug_pull_alert_event
    #     soft_rug_pull_alert_event = TestScamDetector.generate_alert(bot_id, alert_id, description, metadata)

    #     bot_id = "0x98b87a29ecb6c8c0f8e6ea83598817ec91e01c15d379f03c7ff781fd1141e502"
    #     alert_id = "ADDRESS-POISONING"
    #     description = "Possible address poisoning transaction."
    #     metadata = {"attackerAddresses":"0x1a1c0eda425a77fcf7ef4ba6ff1a5bf85e4fc168,0x55d398326f99059ff775485246999027b3197955","anomaly_score":"0.0023634453781512603","logs_length":"24","phishingContract":"0x81ff66ef2097c8c699bff5b7edcf849eb4f452ce","phishingEoa":"0xf6eb5da5850a1602d3d759395480179624cffe2c"}
    #     global address_poisoning_alert_event
    #     address_poisoning_alert_event = TestScamDetector.generate_alert(bot_id, alert_id, description, metadata)

    #     bot_id = "0x1a69f5ec8ef436e4093f9ec4ce1a55252b7a9a2d2c386e3f950b79d164bc99e0"
    #     alert_id = "NIP-1"
    #     description = "0x7cfb946f174807a4746658274763e4d7642233df sent funds to 0x63d8c1d3141a89c4dcad07d9d224bed7be8bb183 with ClaimTokens() as input data"
    #     metadata = {"anomalyScore":"0.000002526532805344122","attacker":"0x63d8c1d3141a89c4dcad07d9d224bed7be8bb183","funcSig":"ClaimTokens()","victim":"0x7cfb946f174807a4746658274763e4d7642233df"}
    #     global nip_alert_event
    #     nip_alert_event = TestScamDetector.generate_alert(bot_id, alert_id, description, metadata)

    #     bot_id = "0xd9584a587a469f3cdd8a03ffccb14114bc78485657e28739b8036aee7782df5c"
    #     alert_id = "SEAPORT-PHISHING-TRANSFER"
    #     description = "3 SewerPass id/s: 19445,25417,5996 sold on Opensea 🌊 for 0.01 ETH with a floor price of 2.5 ETH"
    #     metadata = {"anomaly_score":"0.5","attackHash":"0x016e615428b93eb914ed85aa2bea6962650dfbff6a112edab58ad9ad2fb70640","buyPrice":"0.005","collectionFloor":"14.999","contractAddress":"0xed5af388653567af2f388e6224dc7c4b3241c544","contractName":"Azuki","currency":"ETH","fromAddr":"0x477849ba81b0944f6261bd0fbd24820bce800dc6","hash":"0xd8ddec3d6b10e8e5fe8dddc4535e065e5c19d5d937ffcd493936d6d0a5d25c14","initiator":"0x24278f2643e90b56a519aef6e612d91dca5257d1","itemPrice":"0.005","market":"Opensea 🌊","profit":"0.005","quantity":"2","toAddr":"0x24278f2643e90b56a519aef6e612d91dca5257d1","tokenIds":"9291,9307","totalPrice":"0.01"}
    #     global fraudulent_seaport_orders_alert_event
    #     fraudulent_seaport_orders_alert_event = TestScamDetector.generate_alert(bot_id, alert_id, description, metadata)

    #     bot_id = "0x8badbf2ad65abc3df5b1d9cc388e419d9255ef999fb69aac6bf395646cf01c14"
    #     alert_id = "ICE-PHISHING-HIGH-NUM-APPROVED-TRANSFERS"
    #     description = "0xFB4d3EB37bDe8FA4B52c60AAbE55B3Cd9908EC73 obtained transfer approval for 78 ERC-20 tokens by 195 accounts over period of 4 days."
    #     metadata = {"anomalyScore":"0.00012297740401709194","firstTxHash":"0x5840ac6991b6603de6b05a9da514e5b4d70b15f4bfa36175dd78388915d0b9a9","lastTxHash":"0xf841ffd55ee93da17dd1b017805904ce29c3127dee2db53872234f094d1ce2a0"}
    #     global ice_phishing_alert_event
    #     ice_phishing_alert_event = TestScamDetector.generate_alert(bot_id, alert_id, description, metadata)


    #     #below the alert rates of passhthrough bots across all chains, so very conservative
    #     #wash trading alert rate: 500/day max 
    #     #soft rug pull alert rate: 1000/day max
    #     #hard rug pull alert rate: 300/day max
    #     #rake token alert rate: 10000/day max
    #     #seaport order alert rate: 2000/day max
    #     #ice phishing alert rate: 5000/day max
    #     #address poisoning: 60000/day max
    #     #native ice phishing alert rate: 1000/day max
    #     #alert_detector alert rate: 100/day max
    #     #contract similarity alert rate: 400/day max
    #     #TOTAL: 80000day max

    #     #we have 86400000ms/day, so an alert needs to process in less than 86400000/80000 = 1080ms; given this is for all chains, but there is skew, we multiply that by 2

    #     processing_runs = 10
    #     processing_time_wash_trading_ms = timeit.timeit('agent.detect_scam(w3, wash_trading_alert_event, True)', number=processing_runs, globals=globals()) * 1000 / processing_runs
    #     processing_time_hard_rug_pull_ms = timeit.timeit('agent.detect_scam(w3, hard_rug_pull_alert_event, True)', number=processing_runs, globals=globals()) * 1000 / processing_runs
    #     processing_time_soft_rug_pull_ms = timeit.timeit('agent.detect_scam(w3, soft_rug_pull_alert_event, True)', number=processing_runs, globals=globals()) * 1000 / processing_runs
    #     processing_time_address_poisoning_ms = timeit.timeit('agent.detect_scam(w3, address_poisoning_alert_event, True)', number=processing_runs, globals=globals()) * 1000 / processing_runs
    #     processing_time_fraudulent_seaport_orders_ms = timeit.timeit('agent.detect_scam(w3, fraudulent_seaport_orders_alert_event, True)', number=processing_runs, globals=globals()) * 1000 / processing_runs
    #     processing_time_nip_ms = timeit.timeit('agent.detect_scam(w3, nip_alert_event, True)', number=processing_runs, globals=globals()) * 1000 / processing_runs
    #     processing_time_ice_phishing_ms = timeit.timeit('agent.detect_scam(w3, ice_phishing_alert_event, True)', number=processing_runs, globals=globals()) * 1000 / processing_runs
    #     processing_time_rake_token_ms = timeit.timeit('agent.detect_scam(w3, rake_token_alert_event, True)', number=processing_runs, globals=globals()) * 1000 / processing_runs
    #     processing_time_avg = ((processing_time_wash_trading_ms * (500.0/80000) + processing_time_hard_rug_pull_ms * (300.0/80000) + processing_time_rake_token_ms * (10000.0/80000 +  processing_time_soft_rug_pull_ms * (1000.0/80000)) + 
    #                             processing_time_address_poisoning_ms * (60000.0/80000) + processing_time_fraudulent_seaport_orders_ms * (2000.0/80000) + processing_time_nip_ms * (1000.0/80000 +  processing_time_ice_phishing_ms * (5000.0/80000)))/8)

    #     assert (processing_time_avg/shards) < (1080*2), f"""processing time should be less than {(1080*2)}ms based on the existing sharding config, but is {(processing_time_avg/shards)} ms, 
    #         wash_trading: {processing_time_wash_trading_ms}, 
    #         hard_rug_pull: {processing_time_hard_rug_pull_ms}.
    #         rake_token: {processing_time_rake_token_ms} 
    #         soft_rug_pull: {processing_time_soft_rug_pull_ms} 
    #         nip: {processing_time_nip_ms} 
    #         fraudulent_seaport_orders: {processing_time_fraudulent_seaport_orders_ms} 
    #         address_poisoning: {processing_time_address_poisoning_ms} 
    #         ice_phishing: {processing_time_ice_phishing_ms}
    #         If not, this bot is unlikely to keep up with fast chains, like Polygon"""

    def test_documentation(self):
        # read readme.md

        missing_documentation = ""
        with open("README.md", "r") as f:
            readme = f.read()

            for bot_id, alert_id, alert_logic, alert_id_target in BASE_BOTS:
                found = False
                for line in readme.split("\n"):
                    if bot_id in line and alert_id in line and alert_logic in line:
                        found = True
                # | 0x6aa2012744a3eb210fc4e4b794d9df59684d36d502fd9efe509a867d0efa5127 | token impersonation | IMPERSONATED-TOKEN-DEPLOYMENT-POPULAR | PassThrough |
                if not found:
                    missing_documentation += f"| {bot_id} | | {alert_id} | {alert_logic} |\r\n"
        assert len(missing_documentation) == 0, missing_documentation

    def test_detect_wash_trading(self):
        agent.initialize()
        agent.item_id_prefix = "test_" + str(random.randint(0, 1000000))

        bot_id = "0x067e4c4f771f288c686efa574b685b98a92918f038a478b82c9ac5b5b6472732"
        alert_id = "NFT-WASH-TRADE"
        description = "test Wash Trade on test."
        metadata = {"buyerWallet":"0xa53496B67eec749ac41B4666d63228A0fb0409cf","sellerWallet":"0xD73e0DEf01246b650D8a367A4b209bE59C8bE8aB","anomalyScore":"21.428571428571427% of total trades observed for test are possible wash trades","collectionContract":"test","collectionName":"test","exchangeContract":"test","exchangeName":"test","token":"Wash Traded NFT Token ID: 666688"}
        alert_event = TestScamDetector.generate_alert(bot_id, alert_id, description, metadata)

        findings = TestScamDetector.filter_findings(agent.detect_scam(w3, alert_event, clear_state_flag=True),"passthrough")

        assert len(findings) == 2, "this should have triggered a finding for all two EOAs"
        finding = findings[0]
        assert finding.alert_id == "SCAM-DETECTOR-WASH-TRADE", "should be wash trading finding"
        assert finding.metadata is not None, "metadata should not be empty"
        assert finding.labels is not None, "labels should not be empty"



    def test_detect_impersonation_token(self):
        agent.initialize()
        agent.item_id_prefix = "test_" + str(random.randint(0, 1000000))

        bot_id = "0x6aa2012744a3eb210fc4e4b794d9df59684d36d502fd9efe509a867d0efa5127"
        alert_id = "IMPERSONATED-TOKEN-DEPLOYMENT-POPULAR"
        description = "0x3b31724aff894849b90c48024bab38f25a5ee302 deployed an impersonating token contract at 0xb4d91be6d0894de00a3e57c24f7abb0233814c82. It impersonates token USDC (USDC) at 0x115110423f4ad68a3092b298df7dc2549781108e"
        metadata = {"anomalyScore":"0.09375","newTokenContract":"0xb4d91be6d0894de00a3e57c24f7abb0233814c82","newTokenDeployer":"0x3b31724aff894849b90c48024bab38f25a5ee302","newTokenName":"Cross Chain Token","newTokenSymbol":"USDC","oldTokenContract":"0x115110423f4ad68a3092b298df7dc2549781108e","oldTokenDeployer":"0x80ec4276d31b1573d53f5db75841762607bc2166","oldTokenName":"Cross Chain Token","oldTokenSymbol":"USDC"}
        alert_event = TestScamDetector.generate_alert(bot_id, alert_id, description, metadata)

        findings = TestScamDetector.filter_findings(agent.detect_scam(w3, alert_event, clear_state_flag=True),"passthrough")

        assert len(findings) == 1, "this should have triggered a finding for delpoyer EOA"
        finding = findings[0]
        assert finding.alert_id == "SCAM-DETECTOR-IMPERSONATING-TOKEN", "should be impersonated token finding"
        assert finding.metadata is not None, "metadata should not be empty"
        assert finding.labels is not None, "labels should not be empty"


    def test_detect_hard_rug_pull(self):
        agent.initialize()
        agent.item_id_prefix = "test_" + str(random.randint(0, 1000000))

        bot_id = "0xc608f1aff80657091ad14d974ea37607f6e7513fdb8afaa148b3bff5ba305c15"
        alert_id = "HARD-RUG-PULL-1"
        description = "0x8181bad152a10e7c750af35e44140512552a5cd9 deployed a token contract 0xb68470e3E66862bbeC3E84A4f1993D1d100bc5A9 that may result in a hard rug pull."
        metadata = {"attacker_deployer_address":"0x8181bad152a10e7c750af35e44140512552a5cd9","rugpull_techniques":"HIDDENTRANSFERREVERTS, HONEYPOT","token_contract_address":"0xb68470e3E66862bbeC3E84A4f1993D1d100bc5A9"}
        alert_event = TestScamDetector.generate_alert(bot_id, alert_id, description, metadata)

        findings = TestScamDetector.filter_findings(agent.detect_scam(w3, alert_event, clear_state_flag=True),"passthrough")

        assert len(findings) == 1, "this should have triggered a finding for delpoyer EOA"
        finding = findings[0]
        assert finding.alert_id == "SCAM-DETECTOR-HARD-RUG-PULL", "should be hard rug pull finding"
        assert finding.metadata is not None, "metadata should not be empty"
        assert finding.labels is not None, "labels should not be empty"


    def test_detect_hard_rug_pull_no_repeat_finding(self):
        agent.initialize()
        agent.item_id_prefix = "test_" + str(random.randint(0, 1000000))

        bot_id = "0xc608f1aff80657091ad14d974ea37607f6e7513fdb8afaa148b3bff5ba305c15"
        alert_id = "HARD-RUG-PULL-1"
        description = "0x8181bad152a10e7c750af35e44140512552a5cd9 deployed a token contract 0xb68470e3E66862bbeC3E84A4f1993D1d100bc5A9 that may result in a hard rug pull."
        metadata = {"attacker_deployer_address":"0x8181bad152a10e7c750af35e44140512552a5cd9","rugpull_techniques":"HIDDENTRANSFERREVERTS, HONEYPOT","token_contract_address":"0xb68470e3E66862bbeC3E84A4f1993D1d100bc5A9"}
        alert_event = TestScamDetector.generate_alert(bot_id, alert_id, description, metadata)

        findings = TestScamDetector.filter_findings(agent.detect_scam(w3, alert_event, clear_state_flag=True),"passthrough")

        assert len(findings) == 1, "this should have triggered a finding for delpoyer EOA"
        finding = findings[0]
        assert finding.alert_id == "SCAM-DETECTOR-HARD-RUG-PULL", "should be hard rug pull finding"
        assert finding.metadata is not None, "metadata should not be empty"
        assert finding.labels is not None, "labels should not be empty"

        findings = TestScamDetector.filter_findings(agent.detect_scam(w3, alert_event, clear_state_flag=False),"passthrough")
        assert len(findings) == 0, "this should have not triggered another finding"

    def test_detect_repeat_finding(self):
        agent.initialize()
        agent.item_id_prefix = "test_" + str(random.randint(0, 1000000))

        bot_id = "0xc608f1aff80657091ad14d974ea37607f6e7513fdb8afaa148b3bff5ba305c15"
        alert_id = "HARD-RUG-PULL-1"
        description = "0x8181bad152a10e7c750af35e44140512552a5cd9 deployed a token contract 0xb68470e3E66862bbeC3E84A4f1993D1d100bc5A9 that may result in a hard rug pull."
        metadata = {"attacker_deployer_address":"0x8181bad152a10e7c750af35e44140512552a5cd9","rugpull_techniques":"HIDDENTRANSFERREVERTS, HONEYPOT","token_contract_address":"0xb68470e3E66862bbeC3E84A4f1993D1d100bc5A9"}
        alert_event = TestScamDetector.generate_alert(bot_id, alert_id, description, metadata)

        findings = TestScamDetector.filter_findings(agent.detect_scam(w3, alert_event, clear_state_flag=True),"passthrough")

        assert len(findings) == 1, "this should have triggered a finding for delpoyer EOA"
        finding = findings[0]
        assert finding.alert_id == "SCAM-DETECTOR-HARD-RUG-PULL", "should be hard rug pull finding"
        assert finding.labels is not None, "labels should not be empty"
        assert finding.labels[0].entity == '0x8181bad152a10e7c750af35e44140512552a5cd9'

        bot_id = "0x36be2983e82680996e6ccc2ab39a506444ab7074677e973136fa8d914fc5dd11"
        alert_id = "RAKE-TOKEN-CONTRACT-1"
        description = "swapExactETHForTokensSupportingFeeOnTransferTokens function detected on Uniswap Router to take additional swap fee."
        metadata = {"actualValueReceived":"1.188051244910305019265053e+24","anomalyScore":"0.2226202661207779","attackerRakeTokenDeployer":"0x8181bad152a10e7c750af35e44140512552a5cd9","feeRecipient":"0x440aeca896009f006eea3df4ba3a236ee8d57d36","from":"0x6c07456233f0e0fd03137d814aacf225f528068d","pairAddress":"0x2b25f23c31a490583ff55fb63cea459c098cc0e8","rakeTokenAddress":"0x440aeca896009f006eea3df4ba3a236ee8d57d36","rakeTokenDeployTxHash":"0xec938601346b2ecac1bd82f7ce025037c09a3d817d00d723efa6fc5507bca5c2","rakedFee":"2.09656102042995003399715e+23","rakedFeePercentage":"15.00","totalAmountTransferred":"1.397707346953300022664768e+24"}
        alert_event = TestScamDetector.generate_alert(bot_id, alert_id, description, metadata)

        findings = TestScamDetector.filter_findings(agent.detect_scam(w3, alert_event, clear_state_flag=False),"passthrough")

        assert len(findings) == 1, "this should have triggered a finding for delpoyer EOA for the different alert_id"
        finding = findings[0]
        assert finding.alert_id == "SCAM-DETECTOR-RAKE-TOKEN", "should be hard rug pull finding"
        assert finding.labels is not None, "labels should not be empty"
        assert finding.labels[0].entity == '0x8181bad152a10e7c750af35e44140512552a5cd9'


    def test_detect_rake_token(self):
        agent.initialize()
        agent.item_id_prefix = "test_" + str(random.randint(0, 1000000))

        bot_id = "0x36be2983e82680996e6ccc2ab39a506444ab7074677e973136fa8d914fc5dd11"
        alert_id = "RAKE-TOKEN-CONTRACT-1"
        description = "swapExactETHForTokensSupportingFeeOnTransferTokens function detected on Uniswap Router to take additional swap fee."
        metadata = {"actualValueReceived":"1.188051244910305019265053e+24","anomalyScore":"0.2226202661207779","attackerRakeTokenDeployer":"0xa0f80e637919e7aad4090408a63e0c8eb07dfa03","feeRecipient":"0x440aeca896009f006eea3df4ba3a236ee8d57d36","from":"0x6c07456233f0e0fd03137d814aacf225f528068d","pairAddress":"0x2b25f23c31a490583ff55fb63cea459c098cc0e8","rakeTokenAddress":"0x440aeca896009f006eea3df4ba3a236ee8d57d36","rakeTokenDeployTxHash":"0xec938601346b2ecac1bd82f7ce025037c09a3d817d00d723efa6fc5507bca5c2","rakedFee":"2.09656102042995003399715e+23","rakedFeePercentage":"15.00","totalAmountTransferred":"1.397707346953300022664768e+24"}
        alert_event = TestScamDetector.generate_alert(bot_id, alert_id, description, metadata)

        findings = TestScamDetector.filter_findings(agent.detect_scam(w3, alert_event, clear_state_flag=True),"passthrough")

        assert len(findings) == 1, "this should have triggered a finding for delpoyer EOA"
        finding = findings[0]
        assert finding.alert_id == "SCAM-DETECTOR-RAKE-TOKEN", "should be hard rug pull finding"
        assert finding.metadata is not None, "metadata should not be empty"
        assert finding.labels is not None, "labels should not be empty"
        assert finding.labels[0].entity == '0xa0f80e637919e7aad4090408a63e0c8eb07dfa03'
        assert finding.labels[0].label == 'scammer'
        found_contract = False
        for label in finding.labels:
            if label.entity == '0x440aeca896009f006eea3df4ba3a236ee8d57d36':
                assert label.label == 'scammer'
                found_contract = True   
        assert found_contract, "should have found scammer contract"

    def test_detect_blocksec_phishing_unencrypted(self):
        agent.initialize()
        agent.item_id_prefix = "test_" + str(random.randint(0, 1000000))

        bot_id = "0x9ba66b24eb2113ca3217c5e02ac6671182247c354327b27f645abb7c8a3e4534"
        alert_id = "Ice Phishing"
        description = "Token Transfer Phishing Alert: Scammer (0x0000..9000) profited $168.35931259760338 from phishing. In this transaction, the token (QNT) of the user (0xc1c83d16121bad48ce3e431edd031e741aa6b1e6) was transferred to the address (0x0000553f880ffa3728b290e04e819053a3590000), and the target address was labeled as a phishing address. We believe the user was deceived into a token transfer transaction."
        metadata = {"hash":"0xb5f699cc4d3dba99eba23268aebbcd11384dd33a02f447630116ae4276969f9e","scammer":"0x0000553f880ffa3728b290e04e819053a3590000","victim":"0xc1c83d16121bad48ce3e431edd031e741aa6b1e6"}
        label = {"entity": "0x0000553f880ffa3728b290e04e819053a3590000","entityType": "ADDRESS","label": "phish","metadata": {},"confidence": 1}
        labels = [ label ]
        alert_event = TestScamDetector.generate_alert(bot_id, alert_id, description, metadata, labels)

        findings = TestScamDetector.filter_findings(agent.detect_scam(w3, alert_event, clear_state_flag=True),"passthrough")

        assert len(findings) == 1, "this should have triggered a finding for delpoyer EOA"
        finding = findings[0]
        assert finding.alert_id == "SCAM-DETECTOR-ICE-PHISHING", "should be ice phishing finding"
        assert finding.metadata is not None, "metadata should not be empty"
        assert finding.labels is not None, "labels should not be empty"
        assert finding.labels[0].entity == '0x0000553f880ffa3728b290e04e819053a3590000'
        assert finding.labels[0].label == 'scammer'
        found_contract = False
        for label in finding.labels:
            if label.entity == '0x3eaabef289fdd9072c3ecae94d406c21de881247':
                assert label.label == 'scammer'
                found_contract = True   
        assert found_contract, "should have found scammer contract"

    def test_detect_blocksec_phishing_encrypted(self):
        agent.initialize()
        agent.item_id_prefix = "test_" + str(random.randint(0, 1000000))

        bot_id = "0x9ba66b24eb2113ca3217c5e02ac6671182247c354327b27f645abb7c8a3e4534"
        alert_id = "Ice Phishing"
        description = "Token Transfer Phishing Alert: Scammer (0x0000..9000) profited $168.35931259760338 from phishing. In this transaction, the token (QNT) of the user (0xc1c83d16121bad48ce3e431edd031e741aa6b1e6) was transferred to the address (0x0000553f880ffa3728b290e04e819053a3590000), and the target address was labeled as a phishing address. We believe the user was deceived into a token transfer transaction."
        metadata = {"hash":"0xb5f699cc4d3dba99eba23268aebbcd11384dd33a02f447630116ae4276969f9e","scammer":"0x0000553f880ffa3728b290e04e819053a3590000","victim":"0xc1c83d16121bad48ce3e431edd031e741aa6b1e6"}
        label = {"entity": "0x0000553f880ffa3728b290e04e819053a3590000","entityType": "ADDRESS","label": "phish","metadata": {},"confidence": 1}
        labels = [ label ]
        alert_event = TestScamDetector.generate_alert(bot_id, alert_id, description, metadata, labels)

        encrypted_alert_event = TestScamDetector.encrypt_alert_event(alert_event)

        findings = TestScamDetector.filter_findings(agent.detect_scam(w3, encrypted_alert_event, clear_state_flag=True),"passthrough")

        assert len(findings) == 1, "this should have triggered a finding for delpoyer EOA"
        finding = findings[0]
        assert finding.alert_id == "SCAM-DETECTOR-ICE-PHISHING", "should be ice phishing finding"
        assert finding.metadata is not None, "metadata should not be empty"
        assert finding.labels is not None, "labels should not be empty"
        assert finding.labels[0].entity == '0x0000553f880ffa3728b290e04e819053a3590000'
        assert finding.labels[0].label == 'scammer'
        found_contract = False
        for label in finding.labels:
            if label.entity == '0x3eaabef289fdd9072c3ecae94d406c21de881247':
                assert label.label == 'scammer'
                found_contract = True   
        assert found_contract, "should have found scammer contract"

    def test_detect_soft_rug_pull(self):
        agent.initialize()
        agent.item_id_prefix = "test_" + str(random.randint(0, 1000000))

        bot_id = "0xf234f56095ba6c4c4782045f6d8e95d22da360bdc41b75c0549e2713a93231a4"
        alert_id = "SOFT-RUG-PULL-SUS-LIQ-POOL-RESERVE-CHANGE && SOFT-RUG-PULL-SUS-LIQ-POOL-CREATION"
        description = "Likely Soft rug pull has been detected"
        metadata = {"alert_hash":"0xd99ed20f397dbe53721e9a3424d0b87bcffb8df09fc2a9fea5748f81f3c7d324 && 0x0de8a4f6e1efff58a43cb20a81dd491e23b5eea32412a7b679129eb7b0638ea1","alert_id":"SOFT-RUG-PULL-SUS-LIQ-POOL-RESERVE-CHANGE && SOFT-RUG-PULL-SUS-LIQ-POOL-CREATION","bot_id":"0x1a6da262bff20404ce35e8d4f63622dd9fbe852e5def4dc45820649428da9ea1","contractAddress":"\"0x27382445B936C1f362CbBC32E3d3fa5947220030\"","deployer":"\"0xa3fe18ced8d32ca601e3b4794856c85f6f56a176\"","token":"\"0xdd17532733f084ee4aa2de4a14993ef363843216\"","txHashes":"\"0x136af8104791a904614df3728a4bacf3bb79854db362e70f65e64a787ca23efa\""}
        alert_event = TestScamDetector.generate_alert(bot_id, alert_id, description, metadata)

        findings = TestScamDetector.filter_findings(agent.detect_scam(w3, alert_event, clear_state_flag=True),"passthrough")

        assert len(findings) == 1, "this should have triggered a finding for delpoyer EOA"
        finding = findings[0]
        assert finding.alert_id == "SCAM-DETECTOR-SOFT-RUG-PULL", "should be hard rug pull finding"
        assert finding.metadata is not None, "metadata should not be empty"
        assert finding.labels is not None, "labels should not be empty"
        assert finding.labels[0].entity == '0xa3fe18ced8d32ca601e3b4794856c85f6f56a176'
        assert finding.labels[0].label == 'scammer'
        found_contract = False
        for label in finding.labels:
            if label.entity == '0xdd17532733f084ee4aa2de4a14993ef363843216':
                assert label.label == 'scammer'
                found_contract = True   
        assert found_contract, "should have found scammer contract"


    def test_detect_address_poisoning(self):
        agent.initialize()
        agent.item_id_prefix = "test_" + str(random.randint(0, 1000000))

        bot_id = "0x98b87a29ecb6c8c0f8e6ea83598817ec91e01c15d379f03c7ff781fd1141e502"
        alert_id = "ADDRESS-POISONING"
        description = "Possible address poisoning transaction."
        metadata = {"attackerAddresses":"0x1a1c0eda425a77fcf7ef4ba6ff1a5bf85e4fc168,0x55d398326f99059ff775485246999027b3197954","anomaly_score":"0.0023634453781512603","logs_length":"24","phishingContract":CONTRACT,"phishingEoa":"0xf6eb5da5850a1602d3d759395480179624cffe2c"}
        alert_event = TestScamDetector.generate_alert(bot_id, alert_id, description, metadata)

        findings = TestScamDetector.filter_findings(agent.detect_scam(w3, alert_event, clear_state_flag=True),"passthrough")

        assert len(findings) == 3, "this should have triggered a finding for all three EOAs"
        finding = findings[0]
        assert "SCAM-DETECTOR-ADDRESS-POISON" in finding.alert_id, "should be address poison finding"
        assert finding.metadata is not None, "metadata should not be empty"
        assert finding.labels is not None, "labels should not be empty"



    def test_detect_native_ice_phishing(self):
        agent.initialize()
        agent.item_id_prefix = "test_" + str(random.randint(0, 1000000))

        bot_id = "0x1a69f5ec8ef436e4093f9ec4ce1a55252b7a9a2d2c386e3f950b79d164bc99e0"
        alert_id = "NIP-1"
        description = "0x7cfb946f174807a4746658274763e4d7642233df sent funds to 0x63d8c1d3141a89c4dcad07d9d224bed7be8bb183 with ClaimTokens() as input data"
        metadata = {"anomalyScore":"0.000002526532805344122","attacker":"0x63d8c1d3141a89c4dcad07d9d224bed7be8bb183","funcSig":"ClaimTokens()","victim":"0x7cfb946f174807a4746658274763e4d7642233df"}
        alert_event = TestScamDetector.generate_alert(bot_id, alert_id, description, metadata)

        findings = TestScamDetector.filter_findings(agent.detect_scam(w3, alert_event, clear_state_flag=True),"passthrough")

        assert len(findings) == 1, "this should have triggered a finding"
        finding = findings[0]
        assert finding.alert_id == "SCAM-DETECTOR-SOCIAL-ENG-NATIVE-ICE-PHISHING", "should be soc eng native ice phishing finding"
        assert finding.metadata is not None, "metadata should not be empty"
        assert finding.labels is not None, "labels should not be empty"

    
    def test_detect_ice_phishing_passthrough(self):
        agent.initialize()
        agent.item_id_prefix = "test_" + str(random.randint(0, 1000000))

        bot_id = "0x8badbf2ad65abc3df5b1d9cc388e419d9255ef999fb69aac6bf395646cf01c14"
        alert_id = "ICE-PHISHING-HIGH-NUM-APPROVED-TRANSFERS"
        description = "0xFB4d3EB37bDe8FA4B52c60AAbE55B3Cd9908EC73 obtained transfer approval for 78 ERC-20 tokens by 195 accounts over period of 4 days."
        metadata = {"anomalyScore":"0.00012297740401709194","firstTxHash":"0x5840ac6991b6603de6b05a9da514e5b4d70b15f4bfa36175dd78388915d0b9a9","lastTxHash":"0xf841ffd55ee93da17dd1b017805904ce29c3127dee2db53872234f094d1ce2a0"}
        alert_event = TestScamDetector.generate_alert(bot_id, alert_id, description, metadata)

        findings = TestScamDetector.filter_findings(agent.detect_scam(w3, alert_event, clear_state_flag=True),"passthrough")

        assert len(findings) == 1, "this should have triggered a finding"
        finding = findings[0]
        assert finding.alert_id == "SCAM-DETECTOR-ICE-PHISHING", "should be ice phishing finding"
        assert finding.metadata is not None, "metadata should not be empty"
        assert finding.labels is not None, "labels should not be empty"



    def test_detect_fraudulent_seaport_orders(self):
        agent.initialize()
        agent.item_id_prefix = "test_" + str(random.randint(0, 1000000))

        bot_id = "0x513ea736ece122e1859c1c5a895fb767a8a932b757441eff0cadefa6b8d180ac"
        alert_id = "nft-phishing-sale"
        description = "3 SewerPass id/s: 19445,25417,5996 sold on Opensea 🌊 for 0.01 ETH with a floor price of 2.5 ETH"
        metadata = {"interactedMarket": "opensea","transactionHash": "0x4fff109d9a6c030fce4de9426229a113524903f0babd6de11ee6c046d07226ff","toAddr": "0xBF96d79074b269F75c20BD9fa6DAed0773209EE7","fromAddr": "0x08395C15C21DC3534B1C3b1D4FA5264E5Bd7020C","initiator": "0xaefc35de05da370f121998b0e2e95698841de9b1","totalPrice": "0.001","avgItemPrice": "0.0002","contractAddress": "0xae99a698156ee8f8d07cbe7f271c31eeaac07087","floorPrice": "0.58","timestamp": "1671432035","floorPriceDiff": "-99.97%"}
        alert_event = TestScamDetector.generate_alert(bot_id, alert_id, description, metadata)

        findings = TestScamDetector.filter_findings(agent.detect_scam(w3, alert_event, clear_state_flag=True),"passthrough")

        assert len(findings) == 2, "this should have triggered a finding"
        finding = findings[0]
        assert finding.alert_id == "SCAM-DETECTOR-FRAUDULENT-NFT-ORDER", "should be nft order finding"
        assert finding.metadata is not None, "metadata should not be empty"
        assert finding.labels is not None, "labels should not be empty"


    def test_detect_private_key_compromise(self):
        agent.initialize()
        agent.item_id_prefix = "test_" + str(random.randint(0, 1000000))

        bot_id = "0x6ec42b92a54db0e533575e4ebda287b7d8ad628b14a2268398fd4b794074ea03"
        alert_id = "PKC-2"
        description = "0x006a176a0092b19ad0438919b08a0ed317a2a9b5 transferred funds to 0xdcde9a1d3a0357fa3db6ae14aacb188155362974 and has been inactive for a week"
        metadata = {"anomalyScore":"0.00011111934217349434","attacker":"0xdcde9a1d3a0357fa3db6ae14aacb188155362974","transferredAsset":"MATIC","txHash":"0xd39f161892b9cb184b9daa44d2d5ce4a75ab3133275d5f12a4a2b5eed56b6f41","victims":"0x006a176a0092b19ad0438919b08a0ed317a2a9b5"}
        alert_event = TestScamDetector.generate_alert(bot_id, alert_id, description, metadata)

        findings = TestScamDetector.filter_findings(agent.detect_scam(w3, alert_event, clear_state_flag=True),"passthrough")

        assert len(findings) == 1, "this should have triggered a finding"
        finding = findings[0]
        assert finding.alert_id == "SCAM-DETECTOR-PRIVATE-KEY-COMPROMISE", "should be private key compromise finding"
        assert finding.metadata is not None, "metadata should not be empty"
        assert finding.labels is not None, "labels should not be empty"


    def test_detect_impersonating_token(self):
        agent.initialize()
        agent.item_id_prefix = "test_" + str(random.randint(0, 1000000))

        bot_id = "0x6aa2012744a3eb210fc4e4b794d9df59684d36d502fd9efe509a867d0efa5127"
        alert_id = "IMPERSONATED-TOKEN-DEPLOYMENT-POPULAR"
        description = "0x0cfeaed6f106154153325342d509b3a61b94d68c deployed an impersonating token contract at 0xfbd4f5ce3824af29fcb9e90ccb239f1761670606. It impersonates token BTC (Bitcoin) at 0x05f774f2eca50291a0407ca881f6405d84ea005b"
        metadata = {"anomalyScore":"0.008463572974272662","newTokenContract":"0xfbd4f5ce3824af29fcb9e90ccb239f1761670606","newTokenDeployer":"0x0cfeaed6f106154153325342d509b3a61b94d68c","newTokenName":"Bitcoin","newTokenSymbol":"BTC","oldTokenContract":"0x05f774f2eca50291a0407ca881f6405d84ea005b","oldTokenDeployer":"0x5abf98eb769114e43b1c87413f2a93a384d2e905","oldTokenName":"Bitcoin","oldTokenSymbol":"BTC"}
        alert_event = TestScamDetector.generate_alert(bot_id, alert_id, description, metadata)

        findings = TestScamDetector.filter_findings(agent.detect_scam(w3, alert_event, clear_state_flag=True),"passthrough")

        assert len(findings) == 1, "this should have triggered a finding"
        finding = findings[0]
        assert finding.alert_id == "SCAM-DETECTOR-IMPERSONATING-TOKEN", "should be impersonating token finding"
        assert finding.metadata is not None, "metadata should not be empty"
        assert finding.labels is not None, "labels should not be empty"


    # TODO - fix with new data once version 0.2.8 is deployed and emitted such labels
    def test_detect_alert_similar_contract(self):
        agent.initialize()
        agent.item_id_prefix = "test_" + str(random.randint(0, 1000000))
        
        bot_id = "0x3acf759d5e180c05ecabac2dbd11b79a1f07e746121fc3c86910aaace8910560"
        alert_id = "NEW-SCAMMER-CONTRACT-CODE-HASH"
        description = "0xb48b5b285ecda25e4e06614db34f19ac59ece577 likely involved in a scam (SCAM-DETECTOR-SIMILAR-CONTRACT, propagation)"

        metadata = {"alert_hash":"0x57e0151973e453af21de041ac0ed5bea06f8167da6cfb38240939d6d3b3fd201","new_scammer_contract_address":"0x43abdc640427091f6ce16f68c92775f0c3b4e43b","new_scammer_eoa":"0xb48b5b285ecda25e4e06614db34f19ac59ece577","scammer_contract_address":"0x2874a919b86b7f49f1fa3b53a2a61800a29a6a3b","scammer_eoa":"0xba412a06bb5222861f825363112d452cb4bf1164","similarity_hash":"8b2a9102c1ae5826271f6cf8c5bac3cfd49c524c0838458fa122d0fde374e359","similarity_score":"0.9804986119270325"}
        alert_event = TestScamDetector.generate_alert(bot_id, alert_id, description, metadata)

        findings = agent.detect_scam(w3, alert_event, True)

        assert len(findings) == 1, "this should have triggered a finding"
        assert findings[0].alert_id == "SCAM-DETECTOR-SIMILAR-CONTRACT"
        assert findings[0].metadata['scammer_address'] == "0xb48b5b285ecda25e4e06614db34f19ac59ece577", "metadata should not be empty"
        assert findings[0].metadata['scammer_contract_address'] == "0x43abdc640427091f6ce16f68c92775f0c3b4e43b", "metadata should not be empty"
        assert findings[0].metadata['existing_scammer_address'] == "0xba412a06bb5222861f825363112d452cb4bf1164", "metadata should not be empty"
        assert findings[0].metadata['existing_scammer_contract_address'] == "0x2874a919b86b7f49f1fa3b53a2a61800a29a6a3b", "metadata should not be empty"
        assert findings[0].metadata['similarity_score'] == "0.9804986119270325", "metadata should not be empty"
        assert findings[0].metadata['involved_threat_categories'] == "rake-token", "metadata should not be empty"
        assert findings[0].metadata['involved_alert_hash_1'] == "0x57e0151973e453af21de041ac0ed5bea06f8167da6cfb38240939d6d3b3fd201", "metadata should not be empty"

        assert findings[0].labels is not None, "labels should not be empty"
        label = findings[0].labels[0]
        assert label.entity == "0xb48b5b285ecda25e4e06614db34f19ac59ece577", "entity should be attacker address"
        assert label.label == "similar-contract", "entity should labeled as scam"
        assert label.confidence == 0.4, "entity should labeled with 0.7 confidence"

        label = findings[0].labels[1]
        assert label.entity == "0x43abdc640427091f6ce16f68c92775f0c3b4e43b", "entity should be attacker address"
        assert label.label == "similar-contract", "entity should labeled as scam"
        assert label.confidence == 0.4, "entity should labeled with 0.7 confidence"

    def test_put_entity_cluster(self):
        agent.initialize()
        agent.item_id_prefix = "test_" + str(random.randint(0, 1000000))


        created_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f123Z")
        agent.put_entity_cluster(created_at, EOA_ADDRESS_LARGE_TX, EOA_ADDRESS_LARGE_TX+","+EOA_ADDRESS_SMALL_TX)

        cluster_dict = agent.read_entity_clusters(EOA_ADDRESS_LARGE_TX)
        assert EOA_ADDRESS_LARGE_TX in cluster_dict.keys(), "should have cluster for EOA_ADDRESS_LARGE_TX"
        assert EOA_ADDRESS_LARGE_TX+","+EOA_ADDRESS_SMALL_TX == cluster_dict[EOA_ADDRESS_LARGE_TX]

    def test_put_alert(self):
        agent.initialize()
        agent.item_id_prefix = "test_" + str(random.randint(0, 1000000))

       
        timestamp = 1679508064
        alert = TestScamDetector.generate_alert("0xa91a31df513afff32b9d85a2c2b7e786fdd681b3cdd8d93d6074943ba31ae400", "FUNDING-TORNADO-CASH-4", timestamp=timestamp)
        agent.put_alert(alert, EOA_ADDRESS_SMALL_TX)
        agent.put_alert(alert, EOA_ADDRESS_SMALL_TX)

        alerts = agent.read_alerts(EOA_ADDRESS_SMALL_TX)
        assert len(alerts) == 1, "should be 1 alert"
        assert ("0xa91a31df513afff32b9d85a2c2b7e786fdd681b3cdd8d93d6074943ba31ae400", "FUNDING-TORNADO-CASH-4", "0xabc") in alerts, "should be in alerts"

    def test_put_alert_multiple_shards(self):
        agent.initialize()
        agent.item_id_prefix = "test_" + str(random.randint(0, 1000000))


        timestamp_1 = 1679508064
        shard1 = Utils.get_shard(1, timestamp_1)

        timestamp_2 = timestamp_1 + 1
        shard2 = Utils.get_shard(1, timestamp_2)
        assert shard1 != shard2, "should be different shards"

        alert = TestScamDetector.generate_alert("0xa91a31df513afff32b9d85a2c2b7e786fdd681b3cdd8d93d6074943ba31ae400", "FUNDING-TORNADO-CASH-1", timestamp=timestamp_1)
        agent.put_alert(alert, EOA_ADDRESS_SMALL_TX)

        alert = TestScamDetector.generate_alert("0xa91a31df513afff32b9d85a2c2b7e786fdd681b3cdd8d93d6074943ba31ae400", "FUNDING-TORNADO-CASH-2", timestamp=timestamp_2)
        agent.put_alert(alert, EOA_ADDRESS_SMALL_TX)

        alerts = agent.read_alerts(EOA_ADDRESS_SMALL_TX)
        assert len(alerts) == 2, "should be 2 alert"
        assert ("0xa91a31df513afff32b9d85a2c2b7e786fdd681b3cdd8d93d6074943ba31ae400", "FUNDING-TORNADO-CASH-1", "0xabc") in alerts, "should be in alerts"
        assert ("0xa91a31df513afff32b9d85a2c2b7e786fdd681b3cdd8d93d6074943ba31ae400", "FUNDING-TORNADO-CASH-2", "0xabc") in alerts, "should be in alerts"

    def test_emit_new_manual_finding(self):
        agent.clear_state()
        agent.initialize()
        agent.item_id_prefix = "test_" + str(random.randint(0, 1000000))

        findings = agent.emit_manual_finding(w3, True)
        res = requests.get('https://raw.githubusercontent.com/forta-network/starter-kits/Scam-Detector-ML/scam-detector-py/manual_alert_list.tsv')
        content = res.content.decode('utf-8') if res.status_code == 200 else open('manual_alert_list.tsv', 'r').read()
        df_manual_entries = pd.read_csv(io.StringIO(content), sep='\t')
        assert len(findings) > 0, "this should have triggered manual findings"
        
        for finding in findings:
            address_lower = "0x6939432e462f7dCB6a3Ca39b9723d18a58FE9A65".lower()
            if address_lower in finding.description.lower():
                assert findings[0].alert_id == "SCAM-DETECTOR-MANUAL-ICE-PHISHING", "should be SCAM-DETECTOR-MANUAL-ICE-PHISHING"
                assert findings[0].description == f"{address_lower} likely involved in an attack (SCAM-DETECTOR-MANUAL-ICE-PHISHING, manual)", "wrong description"
                assert findings[0].metadata["reported_by"] == "@CertiKAlert https://twitter.com/CertiKAlert/status/1640288904317378560?s=20"


    #TODO once deployed and those labels with new format coming in
    def test_scammer_contract_deployment(self):
        agent.clear_state()
        agent.initialize()
        agent.item_id_prefix = "test_" + str(random.randint(0, 1000000))

        tx_event = create_transaction_event({
            'transaction': {
                'hash': "0",
                'from': '0x9e187687cea757a65c7438f8cbfc3afa732dffc5',
                'nonce': 9,
            },
            'block': {
                'number': 0
            },
            'receipt': {
                'logs': []}
        })
        findings = agent.detect_scammer_contract_creation(w3, tx_event)

        assert len(findings) == 1, "this should have triggered a finding"
        assert findings[0].alert_id == "SCAM-DETECTOR-SCAMMER-DEPLOYED-CONTRACT"
        assert findings[0].metadata["scammer_contract_address"] == "0xa781690be56b721a61336b5ec5d904417cdab626".lower(), "wrong scammer_contract"

    #TODO once deployed and those labels with new format coming in
    def test_scammer_contract_deployment_indirect(self):
        agent.clear_state()
        agent.initialize()
        agent.item_id_prefix = "test_" + str(random.randint(0, 1000000))

        tx_event = create_transaction_event({
            'transaction': {
                'hash': "0",
                'from': "0x9e187687cea757a65c7438f8cbfc3afa732dffc5",
                'to': "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",
                'nonce': 9,
            },
            'block': {
                'number': 0
            },
            'logs': [
                    {'address': "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f".lower(),
                    'topics': ["0x0d3648bd0f6ba80134a33ba9275ac585d9d315f0ad8355cddefde31afa28d0e9","0x0000000000000000000000008fcbeec40e6926a79c60946544b371773cfa0e78", "0x000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"],
                    'data': f"0x0000000000000000000000002091a6f364e1ea474be9333c6fa3a23ecd604d66000000000000000000000000000000000000000000000000000000000002d7c7"
                 }
            ],
            'receipt': {
                'logs': []
            }
        })
        findings = agent.detect_scammer_contract_creation(w3, tx_event)

        assert len(findings) == 1, "this should have triggered a finding"
        assert findings[0].alert_id == "SCAM-DETECTOR-SCAMMER-DEPLOYED-CONTRACT"
        assert findings[0].metadata["scammer_contract_address"] == "0x2091a6f364e1ea474be9333c6fa3a23ecd604d66".lower(), "wrong scammer_contract"

    def test_detect_eoa_association(self):
        agent.initialize()
        agent.item_id_prefix = "test_" + str(random.randint(0, 1000000))
        
        bot_id = "0xcd9988f3d5c993592b61048628c28a7424235794ada5dc80d55eeb70ec513848"
        alert_id = "SCAMMER-LABEL-PROPAGATION-1"
        description = "0x22914a4f5d97f6a3c4fcc1c44c3a13e567c0efeb marked as scammer by label propagation"
        metadata = {"central_node":"0x13549e22de184a881fe3d164612ef15f99f6d4b3","model_confidence":"0.5","central_node_alert_hash":"0xbda39ad1c0a53555587a8bc9c9f711f0cad81fe89ef235a6d79ee905bc70526c","central_node_alert_id":"SCAM-DETECTOR-ICE-PHISHING","central_node_alert_name":"Scam detector identified an EOA with past alerts mapping to scam behavior","graph_statistics":"[object Object]"}
        alert_event = TestScamDetector.generate_alert(bot_id, alert_id, description, metadata)

        findings = agent.detect_scam(w3, alert_event, True)

        assert len(findings) == 1, "this should have triggered a finding"
        assert findings[0].alert_id == "SCAM-DETECTOR-SCAMMER-ASSOCIATION"
        assert findings[0].labels is not None, "labels should not be empty"
        label = findings[0].labels[0]
        assert label.entity == "0x22914a4f5d97f6a3c4fcc1c44c3a13e567c0efeb", "entity should be attacker address"

    def test_build_feature_vector(self):
        # alerts are tuples of (botId, alertId, alertHash)
        alerts = [('0xbc06a40c341aa1acc139c900fd1b7e3999d71b80c13a9dd50a369d8f923757f5', 'FLASHBOTS-TRANSACTIONS', '0x1'),
                  ('0x8badbf2ad65abc3df5b1d9cc388e419d9255ef999fb69aac6bf395646cf01c14', 'ICE-PHISHING-ERC20-PERMIT', '0x2'),
                  ('0x8badbf2ad65abc3df5b1d9cc388e419d9255ef999fb69aac6bf395646cf01c14', 'ICE-PHISHING-ERC721-APPROVAL-FOR-ALL', '0x3'),
                  ('0x8badbf2ad65abc3df5b1d9cc388e419d9255ef999fb69aac6bf395646cf01c14', 'ICE-PHISHING-ERC721-APPROVAL-FOR-ALL', '0x4')
                  ]

        df_expected_feature_vector = pd.DataFrame(columns=agent.MODEL_FEATURES)
        df_expected_feature_vector.loc[0] = np.zeros(len(agent.MODEL_FEATURES))
        df_expected_feature_vector.iloc[0]["0xbc06a40c341aa1acc139c900fd1b7e3999d71b80c13a9dd50a369d8f923757f5_FLASHBOTS-TRANSACTIONS"] = 1
        df_expected_feature_vector.iloc[0]["0x8badbf2ad65abc3df5b1d9cc388e419d9255ef999fb69aac6bf395646cf01c14_ICE-PHISHING-ERC20-PERMIT"] = 1
        df_expected_feature_vector.iloc[0]["0x8badbf2ad65abc3df5b1d9cc388e419d9255ef999fb69aac6bf395646cf01c14_ICE-PHISHING-ERC721-APPROVAL-FOR-ALL"] = 2
        df_expected_feature_vector.iloc[0]["0xbc06a40c341aa1acc139c900fd1b7e3999d71b80c13a9dd50a369d8f923757f5_count"] = 1
        df_expected_feature_vector.iloc[0]["0xbc06a40c341aa1acc139c900fd1b7e3999d71b80c13a9dd50a369d8f923757f5_uniqalertid_count"] = 1
        df_expected_feature_vector.iloc[0]["0x8badbf2ad65abc3df5b1d9cc388e419d9255ef999fb69aac6bf395646cf01c14_count"] = 3
        df_expected_feature_vector.iloc[0]["0x8badbf2ad65abc3df5b1d9cc388e419d9255ef999fb69aac6bf395646cf01c14_uniqalertid_count"] = 2

        df_expected_feature_vector = df_expected_feature_vector.sort_index(axis=1)  # sort columns alphabetically

        df_feature_vector = agent.build_feature_vector(alerts, EOA_ADDRESS_SMALL_TX)
        assert df_feature_vector.equals(df_expected_feature_vector), "should be equal"

    def test_get_score(self):
        agent.initialize()
        agent.item_id_prefix = "test_" + str(random.randint(0, 1000000))

        df_expected_feature_vector = pd.DataFrame(columns=agent.MODEL_FEATURES)
        df_expected_feature_vector.loc[0] = np.zeros(len(agent.MODEL_FEATURES))

        df_expected_feature_vector.iloc[0]["0x2e51c6a89c2dccc16a813bb0c3bf3bbfe94414b6a0ea3fc650ad2a59e148f3c8_NORMAL-TOKEN-TRANSFERS-TX"] = 1
        df_expected_feature_vector.iloc[0]["0x8badbf2ad65abc3df5b1d9cc388e419d9255ef999fb69aac6bf395646cf01c14_ICE-PHISHING-ERC721-APPROVAL-FOR-ALL"] = 1
        df_expected_feature_vector.iloc[0]["0x8badbf2ad65abc3df5b1d9cc388e419d9255ef999fb69aac6bf395646cf01c14_ICE-PHISHING-HIGH-NUM-APPROVED-TRANSFERS"] = 3
        df_expected_feature_vector.iloc[0]["0x8badbf2ad65abc3df5b1d9cc388e419d9255ef999fb69aac6bf395646cf01c14_ICE-PHISHING-HIGH-NUM-ERC20-APPROVALS"] = 1
        df_expected_feature_vector.iloc[0]["0x8badbf2ad65abc3df5b1d9cc388e419d9255ef999fb69aac6bf395646cf01c14_ICE-PHISHING-SUSPICIOUS-APPROVAL"] = 5
        df_expected_feature_vector.iloc[0]["0xe4a8660b5d79c0c64ac6bfd3b9871b77c98eaaa464aa555c00635e9d8b33f77f_ASSET-DRAINED"] = 3
        df_expected_feature_vector.iloc[0]["0x8badbf2ad65abc3df5b1d9cc388e419d9255ef999fb69aac6bf395646cf01c14_count"] = 10
        df_expected_feature_vector.iloc[0]["0xe4a8660b5d79c0c64ac6bfd3b9871b77c98eaaa464aa555c00635e9d8b33f77f_count"] = 3
        df_expected_feature_vector.iloc[0]["0x2e51c6a89c2dccc16a813bb0c3bf3bbfe94414b6a0ea3fc650ad2a59e148f3c8_count"] = 1

        score = agent.get_model_score(df_expected_feature_vector)
        assert score > MODEL_ALERT_THRESHOLD_LOOSE, "should greater than model threshold"

    def test_get_score_empty_features(self):
        agent.initialize()
        agent.item_id_prefix = "test_" + str(random.randint(0, 1000000))

        df_expected_feature_vector = pd.DataFrame(columns=agent.MODEL_FEATURES)
        df_expected_feature_vector.loc[0] = np.zeros(len(agent.MODEL_FEATURES))
        

        score = agent.get_model_score(df_expected_feature_vector)
        assert score < MODEL_ALERT_THRESHOLD_LOOSE, "should less than model threshold"

    def test_scam_critical(self):
        agent.initialize()
        agent.item_id_prefix = "test_" + str(random.randint(0, 1000000))

        label = {"label": "Scammer",
                 "confidence": 0.25,
                 "entity": "0x2967E7Bb9DaA5711Ac332cAF874BD47ef99B3821",
                 "entityType": EntityType.Address
                 }

        alerts = {"0x2e51c6a89c2dccc16a813bb0c3bf3bbfe94414b6a0ea3fc650ad2a59e148f3c8_NORMAL-TOKEN-TRANSFERS-TX": 1,
                  "0x8badbf2ad65abc3df5b1d9cc388e419d9255ef999fb69aac6bf395646cf01c14_ICE-PHISHING-ERC721-APPROVAL-FOR-ALL": 1
                 }

        timestamp = datetime.now().timestamp()
        all_findings = []
        count = 1
        for alert_key in alerts.keys():
            num_alerts = alerts[alert_key]
            for i in range(num_alerts):
                bot_id = alert_key.split("_")[0]
                alert_id = alert_key.split("_")[1]
                alert_hash = str(hex(count))
                alert_event = TestScamDetector.generate_alert(bot_id=bot_id, alert_id=alert_id, timestamp=int(timestamp), description=EOA_ADDRESS_SMALL_TX, labels=[label], alert_hash=alert_hash)
                findings = TestScamDetector.filter_findings(agent.detect_scam(w3, alert_event, clear_state_flag=False),"ml")
                print(f"bot_id: {bot_id}, alert_id: {alert_id}, findings len: {len(findings)}")
                all_findings.extend(findings)
                count += 1

        assert len(all_findings) == 1
        assert all_findings[0].alert_id == "SCAM-DETECTOR-ICE-PHISHING", "should be SCAM-DETECTOR-ICE-PHISHING"
        assert all_findings[0].severity == FindingSeverity.Critical, "should be Critical"

        assert all_findings[0].labels is not None, "labels should not be empty"
        label = all_findings[0].labels[0]
        assert "ml" == label.metadata['logic']
        assert label.confidence > 0.86 and label.confidence < 0.87, "confidence should be between 0.86 and 0.87"
        



    def test_get_scam_detector_alert_ids(self):
        alert_list = [("0x8badbf2ad65abc3df5b1d9cc388e419d9255ef999fb69aac6bf395646cf01c14", "ICE-PHISHING-ERC20-SCAM-PERMIT", "hash1"), ("0xac82fb2a572c7c0d41dc19d24790db17148d1e00505596ebe421daf91c837799", "ATTACK-DETECTOR-1", "hash2"), ("0xdba64bc69511d102162914ef52441275e651f817e297276966be16aeffe013b0", "UMBRA-RECEIVE", "hash3")]
        expected_result = {"SCAM-DETECTOR-ICE-PHISHING", "SCAM-DETECTOR-1"}

        actual = agent.get_scam_detector_alert_ids(alert_list)
        assert actual == expected_result

    def test_subscription_model_features(self):
        missing_subscription_str = ""
        
        for feature in MODEL_FEATURES:
            botId1 = feature.split("_")[0]
            alertId1 = feature[len(botId1) + 1:]
            if alertId1 == "count" or alertId1 == "uniqalertid_count":
                continue

            found = False
            for botId, alertId, alert_logic, target_alert_id in BASE_BOTS:
                if botId == botId1 and alertId == alertId1:
                    found = True

            if not found:
                missing_subscription_str += f'("{botId1}", "{alertId1}", "Combination", ""),\r\n'
            
        print(missing_subscription_str) 
        assert missing_subscription_str == "", f"Missing subscription for {missing_subscription_str}"


    #TODO - fix once FP labels were generated by a deployed bot
    def test_fp_mitigation_proper_chain_id(self):
        agent.clear_state()
        agent.initialize()
        agent.item_id_prefix = "test_" + str(random.randint(0, 1000000))

        findings = agent.emit_new_fp_finding(w3)
        res = requests.get('https://raw.githubusercontent.com/forta-network/starter-kits/main/scam-detector-py/fp_list.csv')
        content = res.content.decode('utf-8') if res.status_code == 200 else open('fp_list.csv', 'r').read()
        df_fps = pd.read_csv(io.StringIO(content), sep=',')
        assert len(findings) > 0, "this should have triggered FP findings"
        finding = findings[0]
        assert finding.alert_id == "SCAM-DETECTOR-FALSE-POSITIVE", "should be FP mitigation finding"
        assert finding.labels is not None, "labels should not be empty"

    def test_get_similar_contract_labels(self):
        agent.clear_state()
        agent.initialize()
        similar_contract_labels = agent.get_similar_contract_labels(w3, forta_explorer)

        # from_address was detected first and it propagated its label to the to_address
        from_address = "0xfa8c1a1dddea2c06364c9e6ab31772f020f5efc6"
        from_address_deployer = "0x2320a28f52334d62622cc2eafa15de55f9987ecc"
        to_address = "0xfa8c1a1dddea2c06364c9e6ab31772f020f5efc5"
        to_address_deployer = "0x2320a28f52334d62622cc2eafa15de55f9987eaa"

        assert similar_contract_labels[similar_contract_labels['from_entity'] == from_address].iloc[0]['to_entity'] == to_address
        assert similar_contract_labels[similar_contract_labels['from_entity'] == from_address].iloc[0]['from_entity_deployer'] == from_address_deployer
        assert similar_contract_labels[similar_contract_labels['to_entity'] == to_address].iloc[0]['to_entity_deployer'] == to_address_deployer

    def test_get_scammer_association_labels(self):
        agent.clear_state()
        agent.initialize()
        scammer_association_labels = agent.get_scammer_association_labels(w3, forta_explorer)

        # from_address was detected first and it propagated its label to the to_address
        from_address = "0x3805ad836968b7d844eac2fe0eb312ccc37e4630"
        to_address = "0x3805ad836968b7d844eac2fe0eb312ccc37e463a"

        assert scammer_association_labels[scammer_association_labels['from_entity'] == from_address].iloc[0]['to_entity'] == to_address

    def test_obtain_all_fp_labels_deployed_contracts(self):
        # got address EOA_ADDRESS_SMALL_TX that deployed contract CONTRACT
        agent.clear_state()
        agent.initialize()

        similar_contract_labels = pd.DataFrame(columns=['from_entity', 'to_entity'])
        scammer_association_labels = pd.DataFrame(columns=['from_entity', 'to_entity'])

        fp_labels = agent.obtain_all_fp_labels(w3, EOA_ADDRESS_SMALL_TX, block_chain_indexer, forta_explorer, similar_contract_labels, scammer_association_labels, 1)
        sorted_fp_labels = sorted(fp_labels, key=lambda x: x[0])
        sorted_fp_labels = list(sorted_fp_labels)
        assert len(sorted_fp_labels) == 2, "should have two FP label; one for the EOA, one for the contract"
        assert list(sorted_fp_labels)[0][0] == EOA_ADDRESS_SMALL_TX.lower()
        assert 'EOA' in list(sorted_fp_labels)[0][2][0] 
        assert list(sorted_fp_labels)[1][0] == CONTRACT.lower()
        assert 'contract' in list(sorted_fp_labels)[1][2][0] 

    def test_obtain_all_fp_labels_scammer_association(self):
        # got address EOA_ADDRESS_LARGE_TX that was propagated from address EOA_ADDRESS_SMALL_TX
        agent.clear_state()
        agent.initialize()

        similar_contract_labels = pd.DataFrame(columns=['from_entity', 'to_entity'])
        scammer_association_labels = pd.DataFrame(columns=['from_entity', 'to_entity'])
        scammer_association_labels = scammer_association_labels.append({'from_entity': EOA_ADDRESS_LARGE_TX.lower(), 'to_entity': EOA_ADDRESS_SMALL_TX.lower()}, ignore_index=True)

        fp_labels = agent.obtain_all_fp_labels(w3, EOA_ADDRESS_LARGE_TX, block_chain_indexer, forta_explorer, similar_contract_labels, scammer_association_labels, 1)
        sorted_fp_labels = sorted(fp_labels, key=lambda x: x[0])
        sorted_fp_labels = list(sorted_fp_labels)
        assert len(sorted_fp_labels) == 4, "should have three FP labels; one for each EOA and contract"
        assert list(sorted_fp_labels)[0][0] == EOA_ADDRESS_SMALL_TX.lower()
        assert 'EOA' in list(sorted_fp_labels)[0][2][0] 
        assert list(sorted_fp_labels)[3][0] == EOA_ADDRESS_LARGE_TX.lower()
        assert 'EOA' in list(sorted_fp_labels)[3][2][0] 
        
       
    def test_obtain_all_fp_labels_similar_contract(self):
        # got address A that deployed contract B; contract B propagated to contract D
        agent.clear_state()
        agent.initialize()

        similar_contract_labels = pd.DataFrame(columns=['from_entity', 'to_entity'])
        similar_contract_labels = similar_contract_labels.append({'from_entity': CONTRACT.lower(), 'from_entity_deployer': EOA_ADDRESS_LARGE_TX.lower(), 'to_entity_deployer': EOA_ADDRESS_SMALL_TX.lower(), 'to_entity': CONTRACT2.lower()}, ignore_index=True)
        scammer_association_labels = pd.DataFrame(columns=['from_entity', 'to_entity'])
        
        fp_labels = agent.obtain_all_fp_labels(w3, EOA_ADDRESS_LARGE_TX, block_chain_indexer, forta_explorer, similar_contract_labels, scammer_association_labels, 1)
        sorted_fp_labels = sorted(fp_labels, key=lambda x: x[0])
        sorted_fp_labels = list(sorted_fp_labels)
        assert len(sorted_fp_labels) == 4, "should have four FP labels; one for each EOA and contract"