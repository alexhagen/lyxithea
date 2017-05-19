from IPython.display import display, Javascript, HTML

display(Javascript("""
MathJax.Hub.Register.StartupHook("TeX Jax Ready",function () {
  var MML = MathJax.ElementJax.mml,
      TeX = MathJax.InputJax.TeX;

  TeX.Definitions.macros.nicefrac = "myBevelFraction";
  TeX.Definitions.macros.unit = "myUnit";
  TeX.Definitions.macros.ce = "myCe";

  TeX.Parse.Augment({
    myBevelFraction: function (name) {
      var num = this.ParseArg(name),
          den = this.ParseArg(name);
      this.Push(MML.mfrac(num,den).With({bevelled: true}));
    },
    myUnit: function(name) {
      var num = this.ParseArg(name);
      var den = 2;
      this.Push(MML.mtext(num).With({variant: 'normal'}));
    },
    myCe: function(name) {
      var num = this.ParseArg(name);
      var den = 2;
      this.Push(MML.mtext(num).With({variant: 'normal'}));
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

display(HTML('<link rel="stylesheet" href="https://cdn.rawgit.com/tiaanduplessis/wenk/master/dist/wenk.css">'))
