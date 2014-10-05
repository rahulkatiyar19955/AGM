echo
planningTest="basic"
echo "Next: $planningTest"
cd $planningTest
agglplan grammar.aggl initialModel.xml targetModel.xml
cd -
echo "######################################################################"
sleep 1


echo
planningTest="logistics"
echo "Next: $planningTest"
cd $planningTest
agglplan domain1_withCombo.aggl init.xml goal.xml
cd -
echo "######################################################################"
sleep 1


echo
planningTest="logistics 0"
echo "Next: $planningTest"
cd $planningTest
agglplan domain1_withCombo.aggl init0.xml goal0.xml
cd -
echo "######################################################################"
sleep 1


echo
planningTest="logistics 1"
echo "Next: $planningTest"
cd $planningTest
agglplan domain1_withCombo.aggl init1.xml goal1.xml
cd -
echo "######################################################################"
sleep 1


echo
planningTest="logistics 2"
echo "Next: $planningTest"
cd $planningTest
agglplan domain1_withCombo.aggl init2.xml goal2.xml
cd -
echo "######################################################################"
sleep 1


echo
planningTest="makeMeCoffee/navigation/hallToPatio"
echo "Next: $planningTest"
cd $planningTest
agglplan ../../domain.aggl initialModel.xml target.xml
cd -
echo "######################################################################"
sleep 1


echo
echo "######################################################################"
planningTest="makeMeCoffee/perception/findGranny"
echo "Next: $planningTest"
cd $planningTest
agglplan ../../domain.aggl initialModel.xml target.xml
cd -
echo "######################################################################"
sleep 1


echo
planningTest="makeMeCoffee/grasp"
echo "Next: $planningTest 1"
cd $planningTest
agglplan ../domain.aggl initialModel1.xml target1.xml
cd -
echo "######################################################################"
sleep 1


echo
planningTest="makeMeCoffee/grasp"
echo "Next: $planningTest 2"
cd $planningTest
agglplan ../domain.aggl initialModel2.xml target2.xml
cd -
echo "######################################################################"
sleep 1


echo
planningTest="makeMeCoffee/deliver/deliverKnown"
echo "Next: $planningTest 0"
cd $planningTest
agglplan ../../domain.aggl initialModel.xml target0.xml
cd -
echo "######################################################################"
sleep 1


echo
planningTest="makeMeCoffee/deliver/deliverKnown"
echo "Next: $planningTest 1"
cd $planningTest
agglplan ../../domain.aggl initialModel.xml target1.xml
cd -
echo "######################################################################"
sleep 1


echo
planningTest="makeMeCoffee/deliver/deliverKnown"
echo "Next: $planningTest 2"
cd $planningTest
agglplan ../../domain.aggl initialModel.xml target2.xml
cd -
echo "######################################################################"
sleep 1


echo
planningTest="makeMeCoffee/deliver/moveObject"
echo "Next: $planningTest 2"
cd $planningTest
agglplan ../../domain.aggl initialModel.xml target.xml
cd -
echo "######################################################################"
sleep 1


echo
planningTest="makeMeCoffee/hri/coffee 0"
echo "Next: $planningTest"
cd $planningTest
agglplan ../../domain.aggl initialModel.xml target0.xml
cd -
echo "######################################################################"
sleep 1

echo
planningTest="makeMeCoffee/hri/coffee 1"
echo "Next: $planningTest"
cd $planningTest
agglplan ../../domain.aggl initialModel.xml target1.xml
cd -
echo "######################################################################"
sleep 1

echo
planningTest="makeMeCoffee/hri/coffee 2"
echo "Next: $planningTest"
cd $planningTest
agglplan ../../domain.aggl initialModel.xml target2.xml
cd -
echo "######################################################################"
sleep 1

echo
planningTest="makeMeCoffee/hri/coffee 3"
echo "Next: $planningTest"
cd $planningTest
agglplan ../../domain.aggl initialModel.xml target3.xml
cd -
echo "######################################################################"
sleep 1

echo
planningTest="makeMeCoffee/hri/coffee 4"
echo "Next: $planningTest"
cd $planningTest
agglplan ../../domain.aggl initialModel.xml target4.xml
cd -
echo "######################################################################"
sleep 1

echo
planningTest="makeMeCoffee/hri/coffee 5"
echo "Next: $planningTest"
cd $planningTest
agglplan ../../domain.aggl initialModel.xml target5.xml
cd -
echo "######################################################################"
sleep 1

echo
planningTest="makeMeCoffee/hri/coffee 6"
echo "Next: $planningTest"
cd $planningTest
agglplan ../../domain.aggl initialModel.xml target6.xml
cd -
echo "######################################################################"
sleep 1



