package coop.rchain.rosette

import coop.rchain.rosette.Meta.StdMeta

trait RblAtom extends Ob

case class Fixnum(value: Int, override val slot: Seq[Ob] = Seq(StdMeta()))
    extends RblAtom {
  override def toString = s"Fixnum($value)"

  def +(that: Fixnum) = Fixnum(this.value + that.value)

  def -(that: Fixnum) = Fixnum(this.value - that.value)

  def *(that: Fixnum) = Fixnum(this.value * that.value)

  def /(that: Fixnum) = Fixnum(this.value / that.value)
}

case class RoFloat(value: Double, override val slot: Seq[Ob] = Seq(StdMeta()))
    extends RblAtom {
  override def toString: String = s"Float($value)"

  def +(that: RoFloat) = RoFloat(this.value + that.value)

  def -(that: RoFloat) = RoFloat(this.value - that.value)

  def *(that: RoFloat) = RoFloat(this.value * that.value)

  def /(that: RoFloat) = RoFloat(this.value / that.value)
}
