function hideFromUser(x)
{
	//0=admin, 1=registered_user 2=visitor
	if(x == 1 || x == 2)
	{
		var x = document.getElementsByClassName("items-to-hide");
		var i=0;

		while(x[i])
		{
				x[i].style.visibility = "hidden";
				i++
		}
	}

}

//window.onload = hideFromUser();