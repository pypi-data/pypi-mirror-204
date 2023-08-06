// Generated from org/antlr/v4/test/runtime/java/api/VisitorBasic.g4 by ANTLR 4.12.0
package org.antlr.v4.test.runtime.java.api;
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link VisitorBasicParser}.
 */
public interface VisitorBasicListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link VisitorBasicParser#s}.
	 * @param ctx the parse tree
	 */
	void enterS(VisitorBasicParser.SContext ctx);
	/**
	 * Exit a parse tree produced by {@link VisitorBasicParser#s}.
	 * @param ctx the parse tree
	 */
	void exitS(VisitorBasicParser.SContext ctx);
}