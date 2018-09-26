'use strict';
/**
 * Require dependencies
 *
 */
const program = require('commander'),
    chalk = require('chalk'),
    exec = require('child_process'),
    fs = require('fs'),
    pkg = require('./package.json');


let genesis = `
{
    "nonce": "0x0000000000000042",
    "timestamp": "0x0",
    "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "extraData": "0x00",
    "gasLimit": "0x8000000",
    "difficulty": "0x400",
    "mixhash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "coinbase": "0x3333333333333333333333333333333333333333",
    "alloc": {
    },
    "config": { }
}
`;


/**
 * list function definition
 *
 */
let list = (directory,options)  => {
    const cmd = 'ls';
    let params = [];
    
    if (options.all) params.push("a");
    if (options.long) params.push("l");
    let parameterizedCommand = params.length 
                                ? cmd + ' -' + params.join('') 
                                : cmd ;
    if (directory) parameterizedCommand += ' ' + directory ;
    
    let output = (error, stdout, stderr) => {
        if (error) console.log(chalk.red.bold.underline("exec error:") + error);
        if (stdout) console.log(chalk.green.bold.underline("Result:") + stdout);
        if (stderr) console.log(chalk.red("Error: ") + stderr);
    };
    
    exec(parameterizedCommand,output);
    
};

let start = (options)  => {
    const cmd = 'ls';
    let params = [];

    console.log(options)

    let nodePath = options.name
    let genesisPath = nodePath + "/genesis.json"
    exec.execSync("rm -r " + nodePath)
    exec.execSync("mkdir " + nodePath)
	fs.writeFileSync(genesisPath, genesis)

	exec.execSync("geth --datadir " + nodePath + " init " + genesisPath)

	let startCmd = "geth --rpc --rpcport '8545' --rpcaddr localhost --rpcapi='db,eth,net,web3,personal,web3'"
	
    let output = (error, stdout, stderr) => {
        if (error) console.log(chalk.red.bold.underline("exec error:") + error);
        if (stdout) console.log(chalk.green.bold.underline("Result:") + stdout);
        if (stderr) console.log(chalk.red("Error: ") + stderr);
    };

    exec.exec(startCmd)
	// exec.spawn(startCmd, {
 //    	stdio: 'ignore', // piping all stdio to /dev/null
 //    	detached: true
	// }).unref();
    // if (options.all) params.push("a");90;
    // if (options.long) params.push("l");
    // let parameterizedCommand = params.length 
    //                             ? cmd + ' -' + params.join('') 
    //                             : cmd ;
    // if (directory) parameterizedCommand += ' ' + directory ;
    
    // let output = (error, stdout, stderr) => {
    //     if (error) console.log(chalk.red.bold.underline("exec error:") + error);
    //     if (stdout) console.log(chalk.green.bold.underline("Result:") + stdout);
    //     if (stderr) console.log(chalk.red("Error: ") + stderr);
    // };
    
    // exec(parameterizedCommand,output);
    
};



// Main

program
    .command('start')
    .option('-n, --name <value>', 'Node name', 'ethNode0')
    .option('-d, --difficulty <value>', 'Difficulty of mining', '0x400')
    .option('-g, --gasLimit <value>', 'GasLimit', '0x8000000')
    .option('-p, --port <value>','Node port', 30303)
    .option('-c, --passcode <value>','Miner account passcode', '123')
    .action(start);

// console.log(process.argv);
program.parse(process.argv);

// if program was called with no arguments, show help.
if (program.args.length === 0) program.help();
