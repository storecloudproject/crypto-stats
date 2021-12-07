const Web3 = require("web3");

const NODE_URL = "https://speedy-nodes-nyc.moralis.io/4f023a6aa148b1e6a3b48c36/avalanche/mainnet";
const provider = new Web3.providers.HttpProvider(NODE_URL);
const web3 = new Web3(provider);

const blockCount = 1024;

web3.eth.getBlockNumber().then((newestBlock) => {
  web3.eth.getFeeHistory(blockCount, newestBlock, [0]).then((res) => {
    const baseFeePerGas = res.baseFeePerGas;
    console.log(baseFeePerGas);
    // const baseFeePerGasInt = web3.utils.hexToNumber(baseFeePerGas);
    // console.log(baseFeePerGasInt);
  });
});
