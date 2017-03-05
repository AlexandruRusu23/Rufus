window.onload = function()
{
  registerBlock.style.display = 'none';
  loginRecommandation.style.display = 'none';
}


function showRegisterBlock()
{
    registerBlock.style.display = 'block';
    loginRecommandation.style.display = 'block';
    registerRecommandation.style.display = 'none';
    loginBlock.style.display = 'none';
}

function showLoginBlock()
{
  registerBlock.style.display = 'none';
  loginRecommandation.style.display = 'none';
  registerRecommandation.style.display = 'block';
  loginBlock.style.display = 'block';
}
