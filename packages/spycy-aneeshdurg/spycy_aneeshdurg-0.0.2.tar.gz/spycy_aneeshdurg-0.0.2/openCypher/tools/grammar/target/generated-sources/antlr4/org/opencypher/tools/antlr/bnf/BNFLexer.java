// Generated from org/opencypher/tools/antlr/bnf/BNF.g4 by ANTLR 4.7.2
package org.opencypher.tools.antlr.bnf;
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.misc.*;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class BNFLexer extends Lexer {
	static { RuntimeMetaData.checkVersion("4.7.2", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, ASSIGN=2, LBRACE=3, RBRACE=4, LEND=5, REND=6, BAR=7, GT=8, LT=9, 
		ELLIPSIS=10, DOUBLE_EXCLAM=11, DOLLAR=12, ID=13, NORMAL_TEXT=14, SINGLE_LINE_COMMENT=15, 
		INTEGER_LITERAL=16, CHARACTER_LITERAL=17, UNICODE_LITERAL=18, WS=19;
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	private static String[] makeRuleNames() {
		return new String[] {
			"T__0", "ASSIGN", "LBRACE", "RBRACE", "LEND", "REND", "BAR", "GT", "LT", 
			"ELLIPSIS", "DOUBLE_EXCLAM", "DOLLAR", "ID", "NORMAL_TEXT", "SINGLE_LINE_COMMENT", 
			"INTEGER_LITERAL", "CHARACTER_LITERAL", "UNICODE_LITERAL", "HEX_DIGIT", 
			"WS"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'~'", "'::='", "'}'", "'{'", "']'", "'['", "'|'", "'>'", "'<'", 
			"'...'", "'!!'", "'$'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, "ASSIGN", "LBRACE", "RBRACE", "LEND", "REND", "BAR", "GT", 
			"LT", "ELLIPSIS", "DOUBLE_EXCLAM", "DOLLAR", "ID", "NORMAL_TEXT", "SINGLE_LINE_COMMENT", 
			"INTEGER_LITERAL", "CHARACTER_LITERAL", "UNICODE_LITERAL", "WS"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}


	public BNFLexer(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "BNF.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public String[] getChannelNames() { return channelNames; }

	@Override
	public String[] getModeNames() { return modeNames; }

	@Override
	public ATN getATN() { return _ATN; }

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\25x\b\1\4\2\t\2\4"+
		"\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t"+
		"\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22"+
		"\4\23\t\23\4\24\t\24\4\25\t\25\3\2\3\2\3\3\3\3\3\3\3\3\3\4\3\4\3\5\3\5"+
		"\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t\3\n\3\n\3\13\3\13\3\13\3\13\3\f\3\f\3"+
		"\f\3\r\3\r\3\16\3\16\7\16K\n\16\f\16\16\16N\13\16\3\17\3\17\3\17\3\17"+
		"\7\17T\n\17\f\17\16\17W\13\17\3\20\3\20\3\20\3\20\7\20]\n\20\f\20\16\20"+
		"`\13\20\3\20\3\20\3\21\6\21e\n\21\r\21\16\21f\3\22\3\22\3\23\3\23\3\23"+
		"\3\23\3\23\3\23\3\23\3\23\3\24\3\24\3\25\3\25\3\25\3\25\2\2\26\3\3\5\4"+
		"\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33\17\35\20\37\21!\22"+
		"#\23%\24\'\2)\25\3\2\b\4\2C\\c|\b\2\"\"//\62;C\\aac|\4\2\f\f\17\17\n\2"+
		"#$\'\61<=??AB^^`b\u0080\u0080\5\2\62;CHch\5\2\13\f\17\17\"\"\2z\2\3\3"+
		"\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2"+
		"\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3"+
		"\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2"+
		"%\3\2\2\2\2)\3\2\2\2\3+\3\2\2\2\5-\3\2\2\2\7\61\3\2\2\2\t\63\3\2\2\2\13"+
		"\65\3\2\2\2\r\67\3\2\2\2\179\3\2\2\2\21;\3\2\2\2\23=\3\2\2\2\25?\3\2\2"+
		"\2\27C\3\2\2\2\31F\3\2\2\2\33H\3\2\2\2\35O\3\2\2\2\37X\3\2\2\2!d\3\2\2"+
		"\2#h\3\2\2\2%j\3\2\2\2\'r\3\2\2\2)t\3\2\2\2+,\7\u0080\2\2,\4\3\2\2\2-"+
		".\7<\2\2./\7<\2\2/\60\7?\2\2\60\6\3\2\2\2\61\62\7\177\2\2\62\b\3\2\2\2"+
		"\63\64\7}\2\2\64\n\3\2\2\2\65\66\7_\2\2\66\f\3\2\2\2\678\7]\2\28\16\3"+
		"\2\2\29:\7~\2\2:\20\3\2\2\2;<\7@\2\2<\22\3\2\2\2=>\7>\2\2>\24\3\2\2\2"+
		"?@\7\60\2\2@A\7\60\2\2AB\7\60\2\2B\26\3\2\2\2CD\7#\2\2DE\7#\2\2E\30\3"+
		"\2\2\2FG\7&\2\2G\32\3\2\2\2HL\t\2\2\2IK\t\3\2\2JI\3\2\2\2KN\3\2\2\2LJ"+
		"\3\2\2\2LM\3\2\2\2M\34\3\2\2\2NL\3\2\2\2OP\7#\2\2PQ\7#\2\2QU\3\2\2\2R"+
		"T\n\4\2\2SR\3\2\2\2TW\3\2\2\2US\3\2\2\2UV\3\2\2\2V\36\3\2\2\2WU\3\2\2"+
		"\2XY\7\61\2\2YZ\7\61\2\2Z^\3\2\2\2[]\n\4\2\2\\[\3\2\2\2]`\3\2\2\2^\\\3"+
		"\2\2\2^_\3\2\2\2_a\3\2\2\2`^\3\2\2\2ab\b\20\2\2b \3\2\2\2ce\4\62;\2dc"+
		"\3\2\2\2ef\3\2\2\2fd\3\2\2\2fg\3\2\2\2g\"\3\2\2\2hi\t\5\2\2i$\3\2\2\2"+
		"jk\7^\2\2kl\7w\2\2lm\3\2\2\2mn\5\'\24\2no\5\'\24\2op\5\'\24\2pq\5\'\24"+
		"\2q&\3\2\2\2rs\t\6\2\2s(\3\2\2\2tu\t\7\2\2uv\3\2\2\2vw\b\25\3\2w*\3\2"+
		"\2\2\7\2LU^f\4\2\3\2\b\2\2";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}