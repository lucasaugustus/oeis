#! /usr/bin/env python3

# A101765: Iccanobif semiprime indices: Indices of semiprime numbers in A014258.

from labmath import *       # Available via pip (https://pypi.org/project/labmath/)
from multiprocessing import Process, Queue as mpQueue

print("The left column consists of candidates for A101764.")
print("The right column is A014258(k), where k is the value in the left column.")
print("The middle column is the number of digits in the right column.")
print("If a number takes too long to factor, then we automatically move on to the next.")
print()

# To aid verification of the sequence, the following list contains prime factors from the harder-to-factor terms in A014258.

factors = [4756133820311, 152543161050692081, 510936607, 3187722064843, 2608611115351, 9937755559, 38019705991, 461114598713,
           23459098022747, 141700262972823851, 4778004364533087965287, 20011972126882217, 69423904016371, 85115829911419,
           92218932069055425853635483120871, 9398514835298107, 42869587583629, 2723470949877960194785257531005623, 35570102573,
           2082028950669128382210389, 430583442462082639, 1069402726229, 106633963100793179663, 4111224458187349, 2538221024539,
           707440169, 11737619389, 25813522643, 186949792129, 319503601258342728657309177817, 1604501207, 111746836819,
           67143312653, 578459958956737600071750533279, 110576437, 2081960965177, 126646270231946221262624955601, 29490564731,
           35856645529, 2297575978169, 392645755871, 230796900664837350885802966057777973, 21748962373, 594298360555013347,
           1973864333191889, 799790805607, 61441675459, 11523291306424351, 513771778241, 10672608903143791, 516445175203,
           90243287, 327861529, 163848323, 98775373, 358954193443686641785199, 135635909713, 12187804291501, 43011750274860811,
           992844778839553723021, 46907222597880703, 277876722732374268409, 862334384497033633, 583160609, 1129317399653316491,
           10638438704269, 1313597423, 1499295788761, 325895935532257, 734157011726946733, 4840137384259, 6647874806581739,
           40739681, 6013897068703, 13652342192743089733, 7296502709, 107671367, 2580320855755519592093139120859, 17257829,
           1766206961968547189123, 67650865093852049440566516887321, 291274595306516732998969315937, 81869493687446104126921583,
           118131896642586599278321091, 269624699994218931989069726352215760409, 472331627095236291200561, 25297155361445423639,
           471846961372427679150089431613, 3426524956730604411528166991, 31648574251521615319250393099, 281610653, 172320601,
           3625804750570757306291398927, 5069131763288440156816748842770669948308249, 130697537, 64801241, 26227273, 46818353,
           7996589, 66883387, 30149731, 67139687, 81926389]

for p in factors: assert isprime(p)

# We will use multiprocessing to put a timout on each factoring operation.
# Those numbers that hit the timeout were then given special attention by yafu, GMP-ECM, or CADO-NFS.

def extract_prime_factor(x, factors, output):
    # Finds a single prime factor of x, which is returned by putting it into the queue output.
    # Trial divides with each of the elements of factors before passing to primefac.
    for p in factors:
        if x % p == 0:
            output.put(p)
            return
    p = next(primefac(x))
    output.put(p)

a, b = 1, 2
q = mpQueue()
for n in count(3):
    a, b = b, mpz(''.join(reversed(str(a+b))))
    if n in (791, 927, 1022, 1027, 1110, 1129, 1307, 1558, 1662, 1694, 1723, 1747, 1850, 1934, 1954, 1978, 2014, 2069, 2077):
        print('\b'*100 + "%d %d    hard    %d " % (n, len(str(a)), a))
        continue
    print('\b'*100, n, len(str(a)), end=' ', flush=True)
    try:
        proc = Process(target=extract_prime_factor, args=(a, factors, q))
        proc.start()
        proc.join(1)
        if proc.is_alive():
            proc.terminate()
            proc.join()
        if not q.empty():
            p = q.get()
            assert isprime(p)
            assert a % p == 0
        else:
            print('\b'*1000 + "%d %d    timeout    %d " % (n, len(str(a)), a))
            continue
    except KeyboardInterrupt:
        raise
    ap = a // p
    if isprime(ap): print('\b'*1000 + "%d %d %d " % (n, len(str(a)), a))

"""
8 2 93
10 3 415
13 4 9314
17 6 715297
23 5 50689
26 6 734185
28 7 6076767
29 8 88291031
31 8 83760871
39 10 3669611929
42 11 32033758222
53 15 998713689997901
55 16 2056601878063897
56 16 8942319696941409
73 23 35129667777359255138611
83 27 859289765094432585118666889
94 30 793572730750542938887285365311
98 31 9822769628470313494168586499967
101 32 32470004211033025277983987513961
113 35 83219197388484692729128242186175909
114 35 52109855120731775224269012521829661
115 35 75500807452793359764612905250923531
121 37 8530236264991922646919067724466070863
167 51 264432282893527607439092953611813304104409809358771
217 68 20035666302324141753317387563022919586225675656249378003867741071137
255 81 798238398763591009814280968326270931109001066987055315411892017533054297884177577
266 84 682669754255741615680886936034179901156996842999633057629897292024705998026937792489
326 99 226664978294318270528305856795880201127628120064976966378626749369955921194733735237853777380133511
327 99 762417177017909228434909446875396691730659579492653646074497528910047779231385326413502922210000039
333 101 81694393015135847854603014860086026623817539072220184191602358415969850301546496312635576470505860261
367 112 9586178993292195354826279416476446649123619037831661215092188818727843648536136352711772526664840756801050059201
389 120 412801804299940557155410493030777701107604306926132699140934414406668124914028506156512405434885344852689500476543221501
397 123 381311671778000452943921123079357564103718376876091566250563516748419383658612136366462937478589105070089866457017143253581
404 125 42405795645978850070416173550671026630161879890675724233754396131796605205611296802371372265482294932477219119913788309429651
409 126 748855240147639478426101352285631311528128063083257277558649257107392316452369178352010077712897176911291218637402943438412231
423 132 943129503435297716481081237390597407850586978730610804541791806887980972203568617483461395855924086089240700337726915232467543295699
425 131 98939764226468238124048497228836005868970939295466578328907090867424162285515179626347419112024671196367783060300700792709654341269
467 144 849299677631564307509803816959879916569012303672254093777322964953950920910874596513724403579627024228195375242601741217488235674257110525226521
497 150 166643118888739804773607320613905101490883590867688972292744949533913261772405991649884226645201031376862681058544794554969894510604421192503478446921
570 172 2342567041244292358116020463650682300872191194370215088002672818814837030971080509590443963069830727271075211221520151141705718142263450249003034812762024903623542819487453
631 191 26921976986568788518851433849717470206977212433525301854417299813617957593804603827657863106235821415434330652471093182695417294072701696974754305764573160403896934713481542642687429438562171
639 194 88126033453598817162311081563798356774095331154429039601397984037709431047249429550592200586230792375642398468516420563193257168478822367024093532284639813238294979558547666127825509511073991531
749 227 91436994941556873162494871488717214719574554118493219681091550182780861732430803646692126018066750365891171088801026376022675439369593051190307983338043096400820929792032433984178966946825957730939748163626485290928592441836261
761 230 64002363028538571767371692991028393820549512585332812515552384266624682889297730410882219192314375951472830739319667003988009781896950454467948383241730142497456564258461830274440688907143975877499536014095176801001602396678559501
791 239    hard    48424772131393955673155860547372455601394983533754830020014904440505457733225200977954116545002559861443490044572361468801240407886893606252448589856918555620274293995810831936551299054458209474202305219476278455989010829448736626451552521
815 246 182157041154047316250085317823283452517297512530484333098917943030295877132957819677290429971089719858542943350366464616631219992355905993411902329381210607399026039193725132263676810390906577294579886529072997231956955932349987665505741097424411
862 254 93334405405488729277060492012374771445724278581937735732222504872096785194191199461795478191831451716399354739954463204168896710861290799949495614979638228438168297432893616101368993638524369557230744863139026710216944731811566076218004967105812985144727
927 277    hard    7172680090010931754428339024493581762603548241436292231899747868047428183369695966248123253856161277997846445121450661255813986051040701129555897336775663774266855423963773896223950326978440985884388892381981019952155554468124740399801080177978499446051608443195759517715777211
943 281 64773339706155271101751786233275181085732122387370682117901174999831315561604251590536354387100304866206353209231856865862916805313102544400443200840269021484525469236881400134280398556879970375966401845889341703866003718822468937762668657881417111631882052686901867983393047528921
1013 302 49532757112503169550835197004167669512773529438724921741679024666816403361361546296699074603231667785139113267829608462536202704054008643561306815515450208927419135416942202092321047437551915068998559038309527067707336661545191691127663005069190825861934927829072413266831644867705038338778980225524671
1022 304    hard    1468154760916408053401349689736533772019717584666838540504930835122461736803854890322557859871925193704154283666151779469552904222156999482341153640309755040903265216410580549191001711412193058405010425462408666310248841680044026041076765646226086303974068566619721133615254130558961260833119400556282601
1027 304    hard    2015498360805245516856453472299648563788295393102270359176254634151421171215204208977552228571875459298816744768660780560585601447299411906162691523235879415609344846938595505239856992348006534530801257137995360269743147467516954296531938799995699365328562110063747312906623355404157110781076619298657997
1106 326 76076959133111610414942656152610746305403757724051345976914287472027057249503857037611746999016684652259960384166324855736892837764316607477381328829204989676651215980500897546948993316334247672705398481552111994620008365813581927463452690247014677560765888879495455829009040485540474440414612830084373858466818059314867271131
1110 329    hard    25245309006926947866305275686166633683037213637176011265588058982374860122663372643134672758764936816285666179679134894832635712850383996577216907892072149937101152425383117709158975179174063267815332052056604463040467528577997323595953135597513003538229536060645730567715394833636896963853566868383645169677833914330566524485101
1129 333    hard    241681947086509719666444904519322452300895804372892573312339268906002647048894305176791961875532133247138287944626833244006731273241518613225045457822609035672405817844209475228688277214030771501847114359328514384728660971103821387620883125866169826156223183279873958501571851416621611758437338782314591069030126148639851654328493621
1204 357 844501687440616606604291908309968789030451777635043720576698614106716931065735777829437810425448089792410388222237443752730099901010560354305948045581198922084108836343493438932203111757026512481389450487221502466615888341740815381164790454932334048632370258774200845950087430312732324784631868161985500639928287706377954978962058042584310794566327588187819
1307 383    hard    85631971913804234515090117260099128383458163171477874906007717135502549488256409114148985987110514398367588131672125026468651711426950917935150669884861073129981929994791930702636205730235492139668012649906309262118712282483671525923893553748062333735317859482674013137419236774379640257570082426647583523294847103997813019281519932916832552512738114600647383142920766288466436682917
1319 388 9660650394132676970395739547590604418009411780138250883346282117552719024685038445275473016963086070460104914475688015179689768290567596604319396969209167279420348693561105494764635244829626209141617470877329282475686393379831049063893637843323321126582059157277762000034893222449342968162198156337864654013667730759412248787538623413467223003611583972831006306932088769269249225756610751
1398 410 91784740933145143968339227077740898261187367814584530691546572635240403719978493863423010960232699327973932822276083017310662663905248831092846856703340135371148446838319943885691481718262968696679137728800994974439988928289737600280306442180387393590241690607910762104528731954714262213237279537517035265727663388123507883645172508662097612951867429105414347215607344153997277864180041287913552036553975759277
1419 418 8141392628927658864975322221860034669663899944922144906825439745892133063528736057319918557789739020363683539332168000217511075495834085329762989458697784704287236224104462567225052022880654721306951821068948419382118572877508814641464156293693939989136586685644244027315568230851743516916014239394188900825025105143817358965715703743117316696680782780488948498924701380045599857837137006244390927402537641674477626469
1554 461 25135192562098594406972501859992308789168754525851633548030137909715567198177065119524999526949701228601575681632986375943790110025517435089112241856330576038839652882470156641929537304117257991377865682174143802657252142383124284247538368696534446327344630757533649058753573710429063880208250780624989713897409149377388292327009486927883350423495241554164687055098473688581535188822583783888666792040475095349701989869252553062275050351640044150198305707530601
1558 461    hard    18206848503628608927042695322653622396841560171260602423828937345533934760172428126122112463024208530876671701634489467466038991489566378181284858177165277365275185779032573090105539676192497185316576284985611322217309362940158556017636067802666697516931038701807680420128127959589635396561701712835721981179267310093945430241998496328266581883671315715038010398471966194411668811578981511442381110288881545322851199905125319653588198414823259096631027059799321
1662 490    hard    2495019155606498799360575196626657964394079657775988307565437807283376102370758433650257476992455109217536838290681921397221319897781223286141482332244615511309533078915796226460115403769719238140746699322788625324744969386845304303424876344476629836168740360836883535424501803957772063355701668421309509395713021447272249296512542552024008382462509093628435608927649735207832888701887969684746388941920734285928229944971314717899868887487772679261207280889246514586195081500842770378671999
1669 490 8581678289081507006207501428299825503645872943966228872403649948357511326999359074834127527824915930060422253027382234448848685919814905031250346850655219914709227901510937595949976808403642047388137020123237137537514607176656304853278438568772234040314077311653355842328491628823132427229100384965977363178259364938888647450952603379885270896658959961918325731134030129587948669463735081059783541661451090126212571966913777838426104917586750115394312422113695805666785408895959783277320551
1694 495    hard    820436737274350837126483600586235045540077674638159125447420222153155413818133110150715946141778166566669604533392807298981666433262939240276339298890567921422072126852055326206080750125017769415600297480269184326233210992425624849272354282068501958794592000797007159230189631917401581731310989394516658508277467220835744636052733679924902138579576522704141342812473494491702491660228665330501470695836113196717165918338020705771512595592543930416657439014644830434291169843672619008135680564159
1723 502    hard    5164340581085407715463217287762962232221492556570510248008673297988633798175270881535038772115949545903243848742496559880138515672529713615941635494026106207631347213903207597408908364227439267914000300512686957293647954488083367256167160128419240151866370307069348256111691921843418917003649563810060694692127647772541158624405707895996399894248536655165022922223694375616132642500629567122753207439187370324582913796273351007021247138171229753733686238910598863591048124564913079884134480974455876701
1729 504 487381297682284309968295582478055714851845619666893973918898604033640466711925007617383549489589609565308771854113760473090939968749797838512555664510312405583778766710370580426566330972841710726696919831771428500554971108713241664489801536952767957084688249035597922673872775487897965958608229033538050878749713449165797260940771287821586209188687236634856925309538062135031903715793823108328550921791190232384903815844875579688242332426864932842869973696456941328575733008488997443366336403536974568171
1747 507    hard    401426658101647868578497812914597173170385160040924400490897576514542099476419714106890416571922879209586372618118587566092121120170077387684847468217293133377926063117859876119277041705366273480217726519418289679260770763402064949831422550744866534269177775452396960593057013035972659637418096613395010729603157938809313420548264877939941864914109106022868188497054866375644374824176994464408079386087499259997557861554154263657637636389769960701685101301805166962780241076104608895365179566575070062927681
1762 511 1534821419991868882747953734092314586482291429895363688191090561048457388349249494710887182277734457933367777206575675310762768433165810280186567580278075857881212398847809159772497104278126224100815511603323443827399828115825797159332305468407960899501202961939345612020379220646534843811221916261030045083373258213532404264462602023210470534615652959206523621833231458789947502637769527477128083677901641804021160809146817960375080717282918219607749211515065128496340367770747261300712650502634290357813156811
1801 522 766067866501605214596974667012739441853406079507380253641952733124045010183111317903767655725841710028142195901035656978691680692877220816857039220469758941507781253351727009257062000096013624509157340437507873561715382870470035723310380008826953124474679090402156604962685958368780131154039804111125306858808467906250545813041151700444198550710265490277262012101623702783997043378146885444308152858088954546421068892674293784242036261638979487783451089043170825498144375851516526848124810834693559524541870552747370727157
1847 535 8849988755552415098434430032454485793704820921700220448687316465669150056552766942082509406189560172503948790538213571908928326339191149737123322657836497891380175655880224710686233892588772636347217357085816928452202244665604737998547715329835736582989856131393822920666034532808603648220053205569999961120293151991872493207716832178328099043132204794890935353047908491680507342225002021392205672446584126485018764144005775285300465960906477199191500273145263683085615209605757191603690921257214677058903750893408995484007523431980637
1850 537    hard    481743204918972689027159007860171919493624229366307139788704182229931452187281523532923499634765795858920066698430371943362412172401192916443161356483133765287760319517274983330526593293559019727419497525354170672618186338172001059051490454124901645400850454818185405971487878399976636141925196246723294221956428770703351830019164375386418394073164706683432927647951723529263677069028606104131448443607669264039402354766475276622755542023085553658942014945926229872455683754257864931322939722778892331107293955028072374188618850662239211
1874 543 668552525949916127573480145225287296626117833144578567865977581249059231221701451667917965158932458660882885244872224577955484591703671526516822473291289149779689946562506128796106783688311817062015198520795644970910246420327258229967008901295448868684513431118366772983972933580254338318338208689720212649917269485750776547760472648456703077558030985270213716356189638569625671153584564690818055901109289028581417819993419375656917547250987090107268632174924371378872652852663780584991906217855258135383459925090852466840963188823377560325547
1930 555 276435448153894718487662660297387919122620503904539400538753752136568065600268098814363586328749244304251089089786456781123596279602973550176329828108452812620753271068832964720246287079093654377828497759553619819878957119037312722732130289877262674417681864524252289633550102053787309002874695239037812119019821147964337252012689767459370312241820220348287114334004615305653354894469587611607276630559397754405370676663405739118149882435458322712052157032354355431885424676660279020024554160801976873784404200093611976375937353267255611797075108266033151
1934 556    hard    6869181463877708548060663416368522693539365251384594680480480589417134525985265548384174291855223014242649982427718214761179554214185253988255674413903249323064093508131546260353181921483350403261078751672418888862132475372572775170155121080528684095106973882422759576412744648448600042152347384236744474236451211388056345707282088419001501196358543378155537418213860553926084019935803555166872212667713429327023707304126609968322113987306924724862460223038195854865216260316219787758827842153085884835014970067206382544136397073100370122569143222142846009
1954 563    hard    83471192465151916789450294252581758087630946152355097054677905054159760547598760138981528683162777638308293257641756734492194561699107271590932527766323679726458295908975140080975764504907581280606443052004965306602285783725742734030364634736580659151845262104817906939893154247022207097658880091196748292362282518330245207491190713175583224789120763504915004498095348193071429814076259677455081783756195579447014126874097452909192927690261327556152385949409808817274890687993753267892669361895558311136553412827828539380942945734815028564033009747394629581441269
1977 570 693847886996962736767864723397388578111662957844086822145383585692039979805294117983607334732994839293496155099909796710637119917154195657412464975082541935993871216585577883369075340434029023108324998308773761975717802041447246565730706579533630402153939682588900911144259005652959879222793919814994117089344794962114268552997029876175812193076051192072106385199690572021539460413427933664267995850224007405424314588775321339888465842146362465689138767737994360220788948808645289453128563909950883520086953261258425172044149736984986962196627333507835111668855231116379
1978 571    hard    4610819316133703825172018371976656000093908870205469297635384659063503741709687510037014187909540876365323931573271706477130687647537255834911998013835215812949225971319412194814447253348262769053898456666451568639899407340341490086621987456649524098715766380980993030572068127397100416737005367102850005666081132137677156401257816091020451156157133756888927458154608603623784438305132750190801698546950319356605139779888526906323929419761453224145028823530370532279402325387894939102368071905284648808097945286273047014281094068694544408007017308666059656175904119618611
2014 581    hard    92635953618115011432584911134157676947566837496942668191717438161723534900467753118498682517114646734784570586737732983198372575672589312744367332308990451877244740386125606313922410079201924110204416613607052840517170549784410462442090187409497345924936592939423883990261101218861435745892305896365107390563562989116997797508669448015537905807136999494210570427128156763604930271812603596201914335885598062739876332264820997019912695785417645674091895934880457428971487140166660677084707060664305031787602601002320186684828815410182479659238296610949768441793319500215550803639351
2069 599    hard    82375757833983655295554870540801314770054912026866135786712369376309420167540500740754300513020828895447173246334289641080621159036787197939702970304039189934392506280072987157861942669950545517562411454311416860129958945723700145060393512569916472667967395230638328368362756713170973827215744126446690545243405656216567911198046965442624143207984249628289517744409037958812701594947303179122504119525382153008339600592252138089275037116871738019406880707817680614696298572440681161752592020318344960334131032601896266909060755305417440854378251786321141833234039943431822874016096752933047691566781
2077 602    hard    37111441504843013303440698506020899821775391325191014248760895829758463422663660812532689027092836180121341026808512216860668855923321450692626708235020956826346167423519595814597569744832599250840894821143381431004997547470810996632055440371958613858992974198267743638593244513594336575973215021463693837579121416111772037610849383196288432449322649500680604802812393990981549494669753086461026682064172188763773688633925278516065497823498263872444888206292256499931816526840612944480688413746898306494741617040710204346586373000628426130640978418761291934320632609777920408333598843249037689474933101
2123 614 49749085300475453119861171451964595902960901038261149224237937183979057833387210028034163470499783969001568650279194543480035548014358411203504870227306252104702948415832241941471075821530685845318684104549971238891648634160586105041562854493489151558964386417348272082789827720007693577841654017321179835384592697093752132745924241410017736215558128764121374690752436130391814785131632429921871453274968874973483201770083661053997510565077844014011465378805051129012724296143602651803521508363869088240244284512628033399131853824116500468402178324760098810522937500938172544260970659427650485112095480023398993131
"""

# yafu "factor()" -one -pretest 40 -aprcl_p 6021 -aprcl_d 1

