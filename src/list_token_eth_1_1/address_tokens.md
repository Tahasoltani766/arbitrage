###  stETH
> **address :** 0xae7ab96520de3a18e5e111b5eaab095312d7fe84
```bash 
deposit : deposit(uint256 _maxDepositsCount, uint256 _stakingModuleId, bytes _depositCalldata) external {ILidoLocator locator = getLidoLocator()
burn : withdrawWithdrawals(uint256 _amount) external 
```

 ###  Rocket Pool ETH 
> **address :** 0xae78736cd615f374d3085123a210448e74fc6393
```bash
burn : (uint256 _rethAmount) override external
mint: mint(uint256 _ethAmount,address address_to) override external onlyLatestContract
```

 ###  Mantle Staked Ether 
> **address :** 0xd5F7838F5C461fefF7FE49ea5ebaF7728bB0ADfa
```bash
mint : (address staker, uint256 amount) external
burn :(uint256 amount) external
``` 
### Frax Ether
> **address :** 0x5e8422345238f34275888049021821e8e08caa1f
```bash
burn : burn(uint256 amount) public virtual 
minter_mint : minter_mint(address m_address, uint256 m_amount) public onlyMinters
```
### Staked Frax Ether 
> **address :** 0xac3e018457b222d93114458476f3e3416abbe38f
```bash
deposit : deposit(uint256 assets, address receiver) public returns (uint256 shares)
withdraw: withdraw(uint256 assets, address receiver, address owner) public virtual returns (uint256 shares) 
```
### Coinbase Wrapped Staked ETH 
> **address :** 0xbe9895146f7af43049ca1c1ae358b0541ea49704
```bash
 mint : mint(address _to, uint256 _amount) external whenNotPaused onlyMinters notBlacklisted(msg.sender) notBlacklisted(_to) returns (bool)
 burn : burn(uint256 _amount) external whenNotPaused onlyMinters notBlacklisted(msg.sender)
```
### Ankr Staked ETH 
> **address :** 0xe95a203b1a91a908f9b9ce46459d101078c2c3cb
```bash 
mint : mint => mint(address account, uint256 amount) returns (uint256)
burn : burn => burn(address account, uint256 amount) external
```
### Wrapped Beacon ETH 
> **address :** 0xa2E3356610840701BDf5611a53974510Ae27E2e1
```bash 
burn : function requestWithdrawEth(uint256 wbethAmount) external
mint : function mint(address _to, uint256 _amount)

```
### sETH2
> **address :** 0xFe2e637202056d30016725477c5da089Ab0A043A
```bash 
mint :  function mint(uint256 amount) external onlyMinters returns (bool)
burn :  function burn(address account, uint256 amount)
```
