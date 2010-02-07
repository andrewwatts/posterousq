/**
 * a very crude implmentation of python's format() for javascript, 
 * supporting simple replacement fields, eg::
 * 
 *     >>> format('{0} is {1}', 'javascript', 'cool')
 *     "javascript is cool"
 * 
 * works for my purposes, but no where close to implementing full
 * capabilities as described at::
 *       http://docs.python.org/library/string.html#formatstrings
 * 
 */
function format(){

    var formatted_str = arguments[0] || '';

    for(var i=1; i<arguments.length; i++){
        var re = new RegExp("\\{"+(i-1)+"}", "gim");
        formatted_str = formatted_str.replace(re, arguments[i]);
    }
    
    return formatted_str;
}


