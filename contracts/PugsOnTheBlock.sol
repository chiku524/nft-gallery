// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import {ERC721Enumerable} from "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";
import {Strings} from "@openzeppelin/contracts/utils/Strings.sol";

/// @title Pugs On The Block
/// @notice 2,222 peeking pugs for Robinhood Chain (chain ID 4663), OpenSea-ready ERC-721.
contract PugsOnTheBlock is ERC721, ERC721Enumerable, Ownable {
    using Strings for uint256;

    uint256 public constant MAX_SUPPLY = 2222;
    uint256 public mintPrice = 0.004 ether;
    string private _baseTokenURI;
    bool public mintOpen;

    constructor(string memory baseTokenURI_) ERC721("Pugs On The Block", "POTB") Ownable(msg.sender) {
        _baseTokenURI = baseTokenURI_;
    }

    function setMintOpen(bool open) external onlyOwner {
        mintOpen = open;
    }

    function setMintPrice(uint256 price) external onlyOwner {
        mintPrice = price;
    }

    function setBaseURI(string calldata uri) external onlyOwner {
        _baseTokenURI = uri;
    }

    function mint(uint256 quantity) external payable {
        require(mintOpen, "Mint closed");
        require(quantity > 0 && quantity <= 10, "Bad quantity");
        require(totalSupply() + quantity <= MAX_SUPPLY, "Sold out");
        require(msg.value == mintPrice * quantity, "Wrong ETH");

        for (uint256 i = 0; i < quantity; i++) {
            _safeMint(msg.sender, totalSupply() + 1);
        }
    }

    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        _requireOwned(tokenId);
        return string.concat(_baseTokenURI, tokenId.toString(), ".json");
    }

    function withdraw(address payable to) external onlyOwner {
        (bool ok,) = to.call{value: address(this).balance}("");
        require(ok, "Withdraw failed");
    }

    function _update(address to, uint256 tokenId, address auth)
        internal
        override(ERC721, ERC721Enumerable)
        returns (address)
    {
        return super._update(to, tokenId, auth);
    }

    function _increaseBalance(address account, uint128 value) internal override(ERC721, ERC721Enumerable) {
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
