#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import time

from naruno.accounts.get_accounts import GetAccounts
from naruno.accounts.save_accounts import SaveAccounts
from naruno.blockchain.block.block_main import Block
from naruno.blockchain.block.blocks_hash import GetBlockshash
from naruno.blockchain.block.blocks_hash import GetBlockshash_part
from naruno.blockchain.block.blocks_hash import SaveBlockshash
from naruno.blockchain.block.blocks_hash import SaveBlockshash_part
from naruno.blockchain.block.hash.calculate_hash import CalculateHash
from naruno.blockchain.block.save_block import SaveBlock
from naruno.blockchain.candidate_block.candidate_block_main import \
    candidate_block
from naruno.consensus.rounds.round_1.checks.checks_main import \
    round_check
from naruno.lib.log import get_logger
from naruno.node.get_candidate_blocks import GetCandidateBlocks
from naruno.node.server.server import server
from naruno.node.unl import Unl
from naruno.transactions.get_transaction import GetTransaction
from naruno.transactions.process_the_transaction import \
    ProccesstheTransaction

logger = get_logger("CONSENSUS_FIRST_ROUND")


def find_validated(block: Block, candidate_class: candidate_block,
                   unl_nodes: dict) -> list:
    logger.info("Finding process of validating list is started.")
    temp_validating_list = []
    logger.debug(f"First temp_validating_list: {temp_validating_list}")
    for candidate_block in candidate_class.candidate_blocks[:]:
        logger.debug(f"Candidate block {candidate_block}")

        for other_block_tx in candidate_block["transaction"]:

            tx_valid = 1

            if len(candidate_class.candidate_blocks) != 1:

                for other_block in candidate_class.candidate_blocks[:]:
                    if candidate_block["signature"] != other_block["signature"]:

                        for other_block_txs in other_block["transaction"]:
                            if other_block_tx.signature == other_block_txs.signature:

                                tx_valid += 1
            else:
                tx_valid += 1


            logger.debug(
                f"Tx valid of {other_block_tx.signature} : {tx_valid}")
            if tx_valid > ((len(unl_nodes) + 1) / 2):

                already_in_ok = False
                for alrady_tx in temp_validating_list[:]:

                    if other_block_tx.signature == alrady_tx.signature:
                        logger.debug(
                            "The transaction is already in the list")
                        already_in_ok = True
                if not already_in_ok:
                    logger.debug(
                        f"Transaction is valid ({other_block_tx.signature})")
                    temp_validating_list.append(other_block_tx)
    logger.debug(f"First temp_validating_list: {temp_validating_list}")
    return temp_validating_list
