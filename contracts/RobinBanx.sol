// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import {ERC721Enumerable} from "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";
import {Strings} from "@openzeppelin/contracts/utils/Strings.sol";

/// @title Robin Banx
/// @notice A free mint of 10,000 static PNG PFPs on Base (chain ID 8453).
contract RobinBanx is ERC721, ERC721Enumerable, Ownable {
    using Strings for uint256;

    uint256 public constant MAX_SUPPLY = 10_000;
    uint256 public constant MAX_PER_TRANSACTION = 10;
    uint256 public constant MINT_PRICE = 0;

    string private _baseTokenURI;
    bool public mintOpen;

    constructor(string memory baseTokenURI_) ERC721("Robin Banx", "RBX") Ownable(msg.sender) {
        _baseTokenURI = baseTokenURI_;
    }

    function setMintOpen(bool open) external onlyOwner {
        mintOpen = open;
    }

    function setBaseURI(string calldata uri) external onlyOwner {
        _baseTokenURI = uri;
    }

    function mint(uint256 quantity) external payable {
        require(mintOpen, "Mint closed");
        require(quantity > 0 && quantity <= MAX_PER_TRANSACTION, "Bad quantity");
        require(totalSupply() + quantity <= MAX_SUPPLY, "Sold out");
        require(msg.value == MINT_PRICE * quantity, "Mint is free");

        for (uint256 i = 0; i < quantity; ++i) {
            _safeMint(msg.sender, totalSupply() + 1);
        }
    }

    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        _requireOwned(tokenId);
        return string.concat(_baseTokenURI, tokenId.toString(), ".json");
    }

    function _update(address to, uint256 tokenId, address auth)
        internal
        override(ERC721, ERC721Enumerable)
        returns (address)
    {
        return super._update(to, tokenId, auth);
    }

    function _increaseBalance(address account, uint128 value)
        internal
        override(ERC721, ERC721Enumerable)
    {
        super._increaseBalance(account, value);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721Enumerable)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
