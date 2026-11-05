"""Bounded normal/optimized positive and semantic-negative replay."""
import argparse,subprocess,sys,json,pathlib,hashlib,datetime
ROOT=pathlib.Path(__file__).resolve().parent
def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=pathlib.Path);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False)
    cases=[('primary','import optimisation_exact_checks as v;v.main()',True),
      ('independent','import runpy;runpy.run_module("independent_exact_verifier",run_name="__main__")',True),
      ('nine','import optimisation_hinge_n9_exact as v;v.main()',True),
      ('independent-nine','import reviewer_hinge_check as v;v.main()',True),
      ('actual-vector','import actual_vector_series as v;v.main()',True),
      ('nonviolating-horizon','import optimisation_exact_checks as v;from fractions import Fraction as F;v.hinge_case(8,F(2,25),F(10,59),1,F(1,2),F(1))',False),
      ('wrong-matrix','import independent_exact_verifier as v;v.mm=lambda a,b:v.I;v.check_simple_counterexample()',False),
      ('wrong-terminal','import optimisation_hinge_n9_exact as v;v.multiply=lambda a,b:[[v.F(1),v.F(0)],[v.F(0),v.F(1)]];v.main()',False),
      ('wrong-series','import actual_vector_series as v;v.mm=lambda a,b:[[v.O,v.Z],[v.Z,v.O]];v.main()',False),
      ('incompatible-field','import independent_exact_verifier as v;v.Quadratic(1,1,2)+v.Quadratic(1,1,3)',False)]
    # Mutate values only immediately before their intended scientific guard.
    # Earlier branch and D/K checks therefore execute normally and must pass.
    cases += [
      ('terminal-equality-specific', 'import optimisation_hinge_n9_exact as v;import pathlib;source=pathlib.Path(v.__file__).read_text();needle="            require(reflected[0] == delta,";source=source.replace(needle,"            reflected[0] += v.F(1)\\n"+needle);exec(compile(source,v.__file__,"exec"),dict(v=v,__name__="__main__"))',False),
      ('actual-vector-specific', 'import actual_vector_series as v;import pathlib;source=pathlib.Path(v.__file__).read_text();needle="    require(ratio==";source=source.replace(needle,"    ratio[2] += F(1)\\n"+needle);exec(compile(source,v.__file__,"exec"),dict(__name__="__main__"))',False)]
    intended={'terminal-equality-specific':'ArithmeticError: Scientific guard: reflected[0] == delta',
              'actual-vector-specific':'ArithmeticError: Actual vector coefficient mismatch'}
    records=[];positives={}
    for mode,flags in [('normal',[]),('optimized',['-O'])]:
      for name,code,positive in cases:
        command=[sys.executable,'-B',*flags,'-c','import sys;sys.path.insert(0,sys.argv[1]);'+code,str(ROOT)]
        r=subprocess.run(command,capture_output=True,text=True,timeout=60)
        d=a.out/(mode+'-'+name);d.mkdir();(d/'command.json').write_text(json.dumps(command));(d/'stdout.txt').write_text(r.stdout);(d/'stderr.txt').write_text(r.stderr)
        passed=r.returncode==0 if positive else r.returncode!=0 and 'ArithmeticError:' in r.stderr
        if name in intended:
            passed=passed and r.stderr.strip().splitlines()[-1]==intended[name]
        if positive:positives[(mode,name)]=r.stdout
        records.append({'case':d.name,'passed':passed,'returncode':r.returncode,'expectedError':intended.get(name),'hashes':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in d.iterdir()}})
    same=all(positives[('normal',n)]==positives[('optimized',n)] for n,_,b in cases if b)
    result={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'passed':same and all(x['passed'] for x in records),'exactModeAgreement':same,'cases':records,'sourceSha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in ROOT.glob('*.py')},'scope':'Finite examples, coefficients and guard sensitivity; not universal proof or novelty verification'}
    (a.out/'receipt.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));return 0 if result['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
