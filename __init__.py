from IPython.display import display, Javascript, HTML, Markdown, Latex, display_html, display_latex
def html_header():
    html_str = '<span style="display:none;">$\\newcommand{\\unit}[1]{\\mathrm{#1}}$</span>\n'
    html_str += '<span style="display:none;">$\\newcommand{\\ce}[1]{\\mathrm{#1}}$</span>\n'
    html_str += '<link rel="stylesheet" href="https://cdn.rawgit.com/tiaanduplessis/wenk/master/dist/wenk.css">\n'
    html_str += '<style> span.abbr{ color: #999; } </style>\n<style> [data-wenk]:after { z-index: 1000000000; } </style>\n'
    return HTML(html_str)

def javascript_header():
    return Javascript("""
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
    """)

def latex_header():
    latex_string = """
        \\newcommand{\\unit}[1]{\\mathrm{#1}}%
        \\newcommand{\\ce}[1]{\\mathrm{#1}}
    """
    return Latex(latex_string)

html_header()
javascript_header()
latex_header()
