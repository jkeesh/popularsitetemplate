function getVoteCount(itemID, prefix){
	var num = $('#'+prefix+"Number"+itemID).html()
	return parseInt(num);
}


function getPostURL(url, itemID, prefix){
	var posturl = "/" + url + "/" + prefix + "/" + itemID;
	return posturl;
}

function getPrefix(voteType){
	if(voteType == 1)
		return "upvote";
	return "downvote";
}

function getVoteText(prefix, itemID){
	return $('#'+prefix+"Text"+itemID).html();
}

function vote( url, itemID, voteType){
	var prefix = getPrefix(voteType);
	var posturl = getPostURL(url, itemID, prefix)
	
	var prevVotes = getVoteCount(itemID, prefix);
	var newVotes = prevVotes + 1;
	
	$('#'+prefix+itemID).html(getVoteText(prefix,itemID) + " (" + newVotes + ")");
	
	
	$.ajax({
		   type: "POST",
		   url: posturl,
		   success: function(msg){
			//TODO
		   }
		   });
}


function deleteItem(url, itemID){
	var posturl = "/" + url + "/delete/" + itemID;
	$('#item'+itemID).fadeOut("slow");
	$.ajax({
		   type: "POST",
		   url: posturl,
		   success: function(msg){
		   //TODO
		   }
		   });
}





