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


def find_newly(block: Block, temp_validating_list: list) -> list:
    """
    Finds not validated new transaction in our block remove than and return as a new list
    """
    logger.info("Find new transactions process is started")
    newly_added_list = []
    logger.debug(f"First newly_added_list: {newly_added_list}")

    for my_validating_list in block.validating_list[:]:
        ok = any(
            (my_validating_list.signature == my_temp_validating_list.signature)
            for my_temp_validating_list in temp_validating_list[:])

        block.validating_list.remove(my_validating_list)
        logger.info(
            f"tx: {my_validating_list} will removed fron block.validating_list"
        )
        if not ok:
            logger.info(
                f"tx: {temp_validating_list} will added to temp validating list"
            )
            newly_added_list.append(my_validating_list)
    logger.debug(f"End newly_added_list: {newly_added_list}")
    return newly_added_list
