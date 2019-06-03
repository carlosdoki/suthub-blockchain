pragma solidity ^0.4.21;

contract Apolice {
   address public owner;
   bytes32[] public apolices;

   function() public payable {}
   
   function Apolice() public {
      owner = msg.sender;
   }
   
   function kill() public {
      if(msg.sender == owner) selfdestruct(owner);
   }
   
   function checkApoliceIdExists(bytes32 apoliceid) public view returns(bool){
      for(uint256 i = 0; i < apolices.length; i++){
         if(apolices[i] == apoliceid) return true;
      }
      return false;
   } 
   
   function incluiApolice(bytes32 apoliceid) public payable {
       require(!checkApoliceIdExists(apoliceid));
       apolices.push(apoliceid);
   }
   
}
