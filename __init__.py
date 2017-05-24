from IPython.display import display, Javascript, HTML

def header():
    display(Javascript("""
    MathJax.Hub.Register.StartupHook("TeX Jax Ready",function () {
      var MML = MathJax.ElementJax.mml,
          TeX = MathJax.InputJax.TeX;

      TeX.Definitions.macros.nicefrac = "myBevelFraction";

      TeX.Parse.Augment({
        myBevelFraction: function (name) {
          var num = this.ParseArg(name),
              den = this.ParseArg(name);
          this.Push(MML.mfrac(num,den).With({bevelled: true}));
        }
      });
      MathJax.Hub.Insert(MathJax.InputJax.TeX.Definitions.macros,{
          cancel: ["Extension","cancel"],
          bcancel: ["Extension","cancel"],
          xcancel: ["Extension","cancel"],
          cancelto: ["Extension","cancel"]
        });
    });
    """))
    html_str = '<span style="display:none;">$\\newcommand{\\unit}[1]{\\mathrm{#1}}$</span>\n'
    html_str += '<span style="display:none;">$\\newcommand{\\ce}[1]{\\mathrm{#1}}$</span>\n'
    html_str += '<link rel="stylesheet" href="https://cdn.rawgit.com/tiaanduplessis/wenk/master/dist/wenk.css">\n'
    html_str += '<style> span.abbr{ color: #999; } </style>\n<style> [data-wenk]:after { z-index: 1000000000; } </style>\n'
    display(HTML(html_str))
    javascript_str = """
        $('.celltoolbar > .button_container').children('.toggleButton').remove()

        var toggle_button = ("<button class='toggleButton' type='button' value='true'>Show Code</button>");
        $('.celltoolbar > .button_container').append(toggle_button);

        function code_toggle()
        {
            var code_shown = $(this).attr('value') == 'true';
            if (code_shown)
            {
                console.log("code shown")
                $(this).parent().parent().parent().parent().children('.input_area').hide('500');
                $(this).text('Show Code');
            }
            else
            {
                console.log("code not shown")
                $(this).parent().parent().parent().parent().children('.input_area').show('500');
                $(this).text('Hide Code');
            }

            code_shown = !code_shown;
            $(this).attr('value', code_shown);
        }


        $('.toggleButton').each(function() {
            $(this).on('click', code_toggle);
        });
    """
    display(Javascript(javascript_str))

header()
