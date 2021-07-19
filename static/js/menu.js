console.log('hello')
document.getElementById("ham").addEventListener("click",drop)

function drop()
{
    let x = document.getElementsByClassName("navList")[0]
    if (x.style.display == 'flex'){
        x.style.display = 'none'
    }
    else{
        x.style.display = 'flex'
    }
}